# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from ..segmentation import LaplacianThickness
from .test_resampling import change_dir

import os
import pytest


@pytest.fixture()
def change_dir(request):
    orig_dir = os.getcwd()
    filepath = os.path.dirname(os.path.realpath(__file__))
    datadir = os.path.realpath(os.path.join(filepath, '../../../testing/data'))
    os.chdir(datadir)

    def move2orig():
        os.chdir(orig_dir)

    request.addfinalizer(move2orig)


@pytest.fixture()
def create_lt():
    lt = LaplacianThickness()
    # we do not run, so I stick some not really proper files as input
    lt.inputs.input_gm = 'diffusion_weighted.nii'
    lt.inputs.input_wm = 'functional.nii'
    return lt


def test_LaplacianThickness_defaults(change_dir, create_lt):
    lt = create_lt
    base_cmd = 'LaplacianThickness functional.nii diffusion_weighted.nii functional_thickness.nii'
    assert lt.cmdline == base_cmd
    lt.inputs.smooth_param = 4.5
    assert lt.cmdline == base_cmd + " 4.5"
    lt.inputs.prior_thickness = 5.9
    assert lt.cmdline == base_cmd + " 4.5 5.9"
