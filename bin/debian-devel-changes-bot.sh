#!/bin/sh

FIFO="/var/run/debian-devel-changes"
TIMEOUT=5

# Use a temporary file, so we have the option of saving messages
TEMP=$(mktemp /tmp/ddc.XXXXXXXX)
cat - > ${TEMP}

# Send contents of tempfile to FIFO
( cat ${TEMP} > ${FIFO} ) &
PID=$!

# Wait until we have finished writing or timeout
( sleep ${TIMEOUT}; kill ${PID} > /dev/null 2>&1; ) &
wait ${PID}

RET=$?

chmod 666 ${TEMP}
rm -f ${TEMP}

if [ ${RET} -ne 0 ];
then
	# We timed-out, or there was some other error; return
	# "defer" status so we don't lose mail.

	# Postfix's "defer" error code is 75, but Exim's default
	# "defer" codes are 73 and 75, but are configurable with
	# `temp_errors`.

	exit 75
fi
