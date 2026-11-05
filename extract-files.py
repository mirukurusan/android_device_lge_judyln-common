#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    "hardware/qcom-caf/sdm845",
    "vendor/lge/sdm845-common",
    "vendor/qcom/opensource/display",
]


def lib_fixup_system_ext_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_system_ext' if partition in ['system_ext'] else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'liba2dpoffload',
        'libcomprcapture',
        'libhdmiedid',
        'libsndmonitor',
        'libspkrprot',
    ): lib_fixup_remove,
    (
        'libAutoContrast',
        'libarcsoft_beauty_picselfie',
        'libarcsoft_dualcam_portraitlighting',
        'libarcsoft_dualcam_refocus',
        'libarcsoft_dualcam_refocus_front',
        'libarcsoft_dualcam_refocus_rear_t',
        'libarcsoft_makeup',
        'libarcsoft_picselfie_algorithm',
        'libarcsoft_singlecam_portrait_lighting',
        'libcvp2',
        'libcvp2_hfi',
        'libcvp_common',
        'libdepthmapdecoder.arcsoft',
        'liblghdri',
        'libmorpho_image_stab31',
        'libmpbase',
        'libSRIyuv',
        'libc++_shared',
    ): lib_fixup_system_ext_suffix,
}


blob_fixups: blob_fixups_user_type = {
    (
        'vendor/lib/liblgsnpeawb.so',
        'vendor/lib/libSNPE.so'
    ): blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib/libmmcamera_faceproc.so': blob_fixup()
        .clear_symbol_version('__aeabi_memcpy')
        .clear_symbol_version('__aeabi_memset')
        .clear_symbol_version('__gnu_Unwind_Find_exidx'),
}  # fmt: skip


module = ExtractUtilsModule(
    'judyln-common',
    'lge',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
