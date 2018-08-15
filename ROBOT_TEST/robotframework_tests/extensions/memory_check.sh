#!/bin/sh
if [ $# -ne 4 ]
then
        echo -e "Your command line should contain 3 Arguments\n1. Frequency of monitoring Memory in seconds\n2. Max lines in log file\n3. Min lines\n4. Log file name"
        exit
else
        echo "Running MEMORY CHECK every $1 seconds infinitely"
fi

logfile="/common/$4"
logfileCpu="/common/cpu-$4"
echo "Saving logfile at $logfile"
if [ $3 -gt $2 ]
        then
        echo "Max lines cannot be lesser than Min lines, so Inverting the same and continuing the script"
        temp=$2
        temp1=$3
        set -- "$1" "$temp1" "$temp" "$4"
fi
# Collect CPU Details
prev_usr=0
prev_sum=0
do_get_cpu()
{
    result=`cat /proc/stat |grep -w "cpu"`
    usr=`echo $result | tr -s " " |cut -d" " -f2`
    sys=`echo $result | tr -s " " |cut -d" " -f3`
    nic=`echo $result | tr -s " " |cut -d" " -f4`
    idle=`echo $result | tr -s " " |cut -d" " -f5`
    io=`echo $result | tr -s " " |cut -d" " -f6`
    irq=`echo $result | tr -s " " |cut -d" " -f7`
    sirq=`echo $result | tr -s " " |cut -d" " -f8`

    sum=`expr $usr + $sys + $nic + $idle + $io + $irq + $sirq`
    if [ $prev_usr -gt 0 ]; then
        if [ ! -f $logfileCpu ]; then
            echo "Timestamp     Usage" >> $logfileCpu
        fi
        x1=`expr $usr - $prev_usr`
        x2=`expr $sum - $prev_sum`
        x3=`expr $x2 / 100`
        usage=`expr $x1 / $x3`
        echo "$2  $usage" >> $logfileCpu
    fi

    prev_usr=$usr
    prev_sum=$sum
}

while [ 1 ]
    do
        falcon_pid=`ps | grep "falcon -cp" | grep -v "grep" |   tr -s " " |cut -d" " -f1`
        paddy_pids=`ps | grep "paddy" | grep -v "grep" |   tr -s " " |cut -d" " -f1`
        pids_list="$paddy_pids"

        falcon_proc=`ps | grep "falcon -cp" | grep -v "grep" |   tr -s " " |cut -d" " -f5`
        paddy_procs=`ps | grep "paddy" | grep -v "grep" |   tr -s " " |cut -d" " -f7`
        if [$falcon_pid -eq ""]
        then
                falcon_pid=`ps | grep "falcon -cp" | grep -v "grep" |   tr -s " " | sed "s/ //" | cut -d" " -f1`
                paddy_pids=`ps | grep "paddy" | grep -v "grep" |   tr -s " " | sed "s/ //" |cut -d" " -f1`
                pids_list="$paddy_pids"

                falcon_proc=`ps | grep "falcon -cp" | grep -v "grep" |   tr -s " " | sed "s/ //" | cut -d" " -f5`
                paddy_procs=`ps | grep "paddy" | grep -v "grep" |   tr -s " " | sed "s/ //" | cut -d" " -f7`
        fi
        system_memory=""
        paddy_list=""
        memory_list=""
        mytime=`date +"%s"`
        if [ ! -f $logfile ]
        then
                for paddy in $paddy_procs
                do
                        paddy_list="${paddy_list}    ${paddy}"
                done
                echo "Timestamp    Falcon    System    $paddy_list" > $logfile
                chmod 644 $logfile
        fi

        for pid in $pids_list
        do
                memory=`cat /proc/$pid/status | grep VmRSS | tr -s " " | cut -d" " -f2-`
                memory_list="${memory_list}    ${memory}"
        done
        falcon_memory=`cat /proc/$falcon_pid/status | grep VmRSS | tr -s " " | cut -d" " -f2-`
        system_memory_total=`cat /proc/meminfo | grep MemTotal | cut -d: -f2 | sed 's/kB//'`
        system_memory_free=`cat /proc/meminfo | grep MemFree | cut -d: -f2 | sed 's/kB//'`
        system_memory=`expr $system_memory_total - $system_memory_free`
        echo "$mytime    $falcon_memory    $system_memory    $memory_list" >> $logfile
        sed -i "s/[kK][bB]//g" $logfile
        mydate=`date +%m%d%Y`
        do_get_cpu $mydate $mytime
        sleep $1
        lines=`cat $logfile | wc -l`
        cpulines=`cat $logfileCpu | wc -l`

        echo " Total lines : $lines"
        echo " Total CPU lines : $cpulines"
        if [ $lines -gt $2 ]
        then
                lower_line_count=$(expr $lines - $3)
                echo " Deleting $lower_line_count lines from log file"
                sed -i "2,$lower_line_count d" $logfile
        fi
        if [ $cpulines -gt $2 ]
        then
                lower_line_count_cpu=$(expr $cpulines - $3)
                echo " Deleting $lower_line_count_cpu lines from cpu log file"
                sed -i "2,$lower_line_count_cpu d" $cpulines
        fi
                echo " after $1 seconds"
    done
