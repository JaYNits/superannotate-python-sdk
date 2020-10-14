import pydicom.data

import superannotate as sa


def test_dicom_convesion(tmpdir):
    sa.dicom_to_rgb_sequence(
        pydicom.data.get_testdata_file("CT_small.dcm"), tmpdir
    )
