##############################################################################
#
# Copyright (c) 2006-2011 Curictus AB.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##############################################################################

import os, sys
import logging

##############################################################################
# Dump hardware GUID.
##############################################################################

def main(is_frozen, rootdir):
    try:
        from vrs.config import Config
        config = Config()
        print config.HARDWARE_GUID
        open("hardwareid.txt", "wt").write(config.HARDWARE_GUID)
    except KeyboardInterrupt:
        pass

    
##############################################################################
# Entry-point.
##############################################################################

is_frozen = hasattr(sys, "frozen")
        
if __name__ == '__main__':
    if is_frozen:
        rootdir = os.path.abspath(os.path.dirname(sys.executable))
    else:
        rootdir = os.path.abspath(os.path.dirname(__file__))

    if not is_frozen:
        sys.path.append(os.path.join(rootdir, "../../Curegame/modules"))

    try:
        main(is_frozen, rootdir)
    except SystemExit:
        pass
    except:
        logging.exception("Unhandled exception")

    
##############################################################################
# The End.
##############################################################################
