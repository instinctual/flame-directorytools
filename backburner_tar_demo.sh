#!/bin/sh

#manager= Backburner Manager IP or hostname
#group= Backburner Group to send job to
#jobName=Name that shows up in Backburner Monitor
#priority=priority of job in queue.  Lower # is higher priority
#userRights=run job as user submitting.  Without this job runs as root.
#description= Description that shows up in BB Monitor
#Simple explanation.  Tar a folder, excluding its parents, then list the contents of
#the tar and sort it so it is in numberical order, put that to a human readable file

TARDIR=$1
BBMANAGER=manager
BBGROUP=TARNODES
CMDJOB=/opt/Autodesk/backburner/cmdjob
$CMDJOB -manager:$BBMANAGER -group:$BBGROUP -priority:30 -jobName "`basename $TARDIR` DCDM" -userRights -description "TAR + List file" sh -c "/usr/bin/tar -cvf $TARDIR.tar -C `dirname $TARDIR` `basename $TARDIR` ; tar -tvf $TARDIR.tar | sort > $TARDIR.tar.list"
