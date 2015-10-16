#!/bin/sh

base_path=$(cd `dirname $(readlink $0)`; pwd)
ndk_path=/cygdrive/d/Android/ndk/android-ndk-r10e/

if [ ! -e vmlinux ]
then
	echo "no vmlinux, exit"
	exit 1;
fi

echo "msm8992 ram parser AP start" 
rm -rf ap-log
mkdir ap-log

python $base_path/./ramparse.py \
	--nm-path $ndk_path/toolchains/aarch64-linux-android-4.9/prebuilt/windows-x86_64/bin/aarch64-linux-android-nm \
	--gdb-path $ndk_path/toolchains/aarch64-linux-android-4.9/prebuilt/windows-x86_64/bin/aarch64-linux-android-gdb \
	--vmlinux ./vmlinux \
	-a . \
	--outdir ./ap-log \
	-x --64-bit --force-hardware 8992
echo "msm8992 ram parser AP done" 

#echo "msm8992 ram parser TZ start" 
#python $base_path/tz_diag_parser.py OCIMEM.BIN DDRCS0_0.BIN > ./ap-logs/tz_log.txt
#echo "msm8992 ram parser TZ done" 
#
#if [ -e RPM_AAAAANAAR.elf ]
#then
#    rm -rf rpm-log
#    mkdir rpm-log
# 
#    python "$oem_root_path"/rpm_proc/core/bsp/rpm/scripts/hansei/hansei.py --elf ./RPM_AAAAANAAR.elf -o ./rpm-logs/ ./CODERAM.BIN ./DATARAM.BIN ./MSGRAM.BIN
#fi
