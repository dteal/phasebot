#pragma GCC diagnostic ignored "-Wnarrowing"

/*
 * This file is part of the OpenKinect Project. http://www.openkinect.org
 *
 * Copyright (c) 2011 individual OpenKinect contributors. See the CONTRIB file
 * for details.
 *
 * This code is licensed to you under the terms of the Apache License, version
 * 2.0, or, at your option, the terms of the GNU General Public License,
 * version 2.0. See the APACHE20 and GPL2 files for the text of the licenses,
 * or the following URLs:
 * http://www.apache.org/licenses/LICENSE-2.0
 * http://www.gnu.org/licenses/gpl-2.0.txt
 *
 * If you redistribute this file in source form, modified or unmodified, you
 * may:
 *   1) Leave this header intact and distribute it under the same terms,
 *      accompanying it with the APACHE20 and GPL20 files, or
 *   2) Delete the Apache 2.0 clause and accompany it with the GPL2 file, or
 *   3) Delete the GPL v2 clause and accompany it with the APACHE20 file
 * In all cases you must keep the copyright notice intact and include a copy
 * of the CONTRIB file.
 *
 * Binary distributions must follow the binary distribution requirements of
 * either License.
 */

#include "libfreenect.h"
#include "libfreenect_audio.h"
#include <stdio.h>
#include <signal.h>
#include <Python.h>

static PyObject * python_audio_callback = NULL; // to be called with audio packets
static freenect_context * f_ctx;
static freenect_device * f_dev;
int die = 0;

typedef struct {
	FILE* logfiles[4];
	int samples;
} capture;

// internal new data callback
void in_callback(freenect_device* dev, int num_samples,
                 int32_t* mic1, int32_t* mic2,
                 int32_t* mic3, int32_t* mic4,
                 int16_t* cancelled, void *unknown) {
	capture* c = (capture*)freenect_get_user(dev);
	//fwrite(mic1, 1, num_samples*sizeof(int32_t), c->logfiles[0]);
	//fwrite(mic2, 1, num_samples*sizeof(int32_t), c->logfiles[1]);
	//fwrite(mic3, 1, num_samples*sizeof(int32_t), c->logfiles[2]);
	//fwrite(mic4, 1, num_samples*sizeof(int32_t), c->logfiles[3]);
	c->samples += num_samples;
	printf("Sample received 1. Total samples recorded: %d\n", c->samples);
    
    for(int i=0; i<num_samples; i++){
        PyObject *arglist;
        int arg1 = mic1[0];
        int arg2 = mic1[0];
        int arg3 = mic3[0];
        int arg4 = mic4[0];
        arglist = Py_BuildValue("iiii", arg1,arg2,arg3,arg4);
        PyObject_CallObject(python_audio_callback, arglist);
        Py_DECREF(arglist);
    }

}

// internal cleanup callback
void cleanup(int sig) {
	printf("Caught SIGINT, cleaning up\n");
	die = 1;
}

// initializes module, registers callback, starts playback immediately
static PyObject* init_audio(PyObject *self, PyObject *args) {

    // first, get Python function to call back with audio data
    PyObject *result = NULL;
    PyObject *temp;
    if (PyArg_ParseTuple(args, "O:set_callback", &temp)) {
        if (!PyCallable_Check(temp)) {
            PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            return NULL;
        }
        Py_XINCREF(temp);         /* Add a reference to new callback */
        Py_XDECREF(python_audio_callback);  /* Dispose of previous callback */
        python_audio_callback = temp;       /* Remember new callback */
        /* Boilerplate to return "None" */
        Py_INCREF(Py_None);
        result = Py_None;
    }

    // next, initialize freenect
	if (freenect_init(&f_ctx, NULL) < 0) {
		printf("freenect_init() failed\n");
        return Py_BuildValue("s", "Kinect audio initialization failed!");
	}
	freenect_set_log_level(f_ctx, FREENECT_LOG_SPEW);
	freenect_select_subdevices(f_ctx, FREENECT_DEVICE_AUDIO);
	int nr_devices = freenect_num_devices (f_ctx);
	printf ("Number of devices found: %d\n", nr_devices);
	if (nr_devices < 1) {
		freenect_shutdown(f_ctx);
        return Py_BuildValue("s", "No devices found!");
	}
	int user_device_number = 0;
	if (freenect_open_device(f_ctx, &f_dev, user_device_number) < 0) {
		printf("Could not open device\n");
		freenect_shutdown(f_ctx);
        return Py_BuildValue("s", "Could not open device!");
	}

    // finally, start the device
	capture state;
	state.samples = 0;
	freenect_set_user(f_dev, &state);
	freenect_set_audio_in_callback(f_dev, in_callback);
	freenect_start_audio(f_dev);
	signal(SIGINT, cleanup);

    while(!die && freenect_process_events(f_ctx) >= 0) {
    }

	freenect_shutdown(f_ctx);
    return result;
}


static PyMethodDef module_methods[] = {
    {"init_audio", init_audio, METH_VARARGS, "initializes and starts kinect audio with callback"},
    {NULL}
};

static struct PyModuleDef freenectaudiomodule = {
    PyModuleDef_HEAD_INIT,
    "freenectaudio",
    "exposes libfreenect audio to Python",
    -1,
    module_methods
};

PyMODINIT_FUNC PyInit_freenectaudio(void) {
    return PyModule_Create(&freenectaudiomodule);
}