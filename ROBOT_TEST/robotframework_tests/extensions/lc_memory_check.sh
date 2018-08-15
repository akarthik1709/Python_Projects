#!/bin/sh
if [ $# -ne 4 ]
then
        echo -e "Your command line should contain 4 Arguments\n1. Frequency of monitoring Memory in seconds\n2. Max lines in log file\n3. Min lines\n4. Log file name"
        exit
else
        echo "Running MEMORY CHECK every $1 seconds infinitely"
fi

logfile="/etc/idirect/lc-$4"           # $4 is the .csv file name different. timestamp-falcon-system-hua-piculet. path is diff
logfileCpu="/etc/idirect/lc-cpu-$4"    # log collects timestamp and cpu readings. path is diff
echo "Saving logfile at $logfile"
if [ $3 -gt $2 ]
        then
        echo "Max lines cannot be lesser than Min lines, so Inverting the same and continuing the script"
        temp=$2
        temp1=$3
        set -- "$1" "$temp1" "$temp" "$4"
fi
# Collect LC CPU Details - all similar to original here
prev_usr=0
prev_sum=0

do_get_cpu()
{
    result=`cat /proc/stat |grep -w "cpu"`                        # CPU fetching command - same as for remote
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


while [ 1 ]              # timestamp-falcon-system-hua-piculet
    do
        falcon_pid=`ps | grep "falcon" | grep -v "grep" |   tr -s " " | sed "s/ //" | cut -d" " -f1 | cut -c1-5`
        hua_pid=`ps | grep "hua -cp" | grep -v "grep" |   tr -s " " | sed "s/ //" | cut -d" " -f1 | cut -c1-5`
        piculet_pid=`ps | grep "piculet -cp" | grep -v "grep" |   tr -s " " | sed "s/ //" | cut -d" " -f1 | sed -n '3!p' | sed -n '2!p' | cut -c1-5`

        falcon_proc=`ps | grep "falcon" | grep -v "grep" |   tr -s " " | sed "s/ //" | cut -d" " -f4`
        hua_proc=`ps | grep "hua -cp" | grep -v "grep" |   tr -s " " | sed "s/ //" | cut -d" " -f4`
        piculet_proc=`ps | grep "piculet -cp" | grep -v "grep" |   tr -s " " | sed "s/ //" | cut -d" " -f4`

        system_memory=""
        memory_list=""
        mytime=`date +"%s"`
        if [ ! -f $logfile ]
        then
                echo "Timestamp    Falcon    System    HUA    Piculet" > $logfile
                chmod 644 $logfile
        fi

        falcon_memory=`cat /proc/$falcon_pid/status | grep VmRSS | tr -s " " | cut -d" " -f2- | sed s/kB//`    # fecth falcon used memory
        if [ "$falcon_memory" == "" ]; then
                falcon_memory='0'
        fi
        hua_memory=`cat /proc/$hua_pid/status | grep VmRSS | tr -s " " | cut -d" " -f2- | sed s/kB//`          # fecth hua used memory
        if [ "$hua_memory" == "" ]; then
                hua_memory='0'
        fi
        piculet_memory=`cat /proc/$piculet_pid/status | grep VmRSS | tr -s " " | cut -d" " -f2- | sed s/kB//`  # fecth piculet used memory
        if [ "$piculet_memory" == "" ]; then
                piculet_memory='0'
        fi
        system_memory_total=`cat /proc/meminfo | grep MemTotal | cut -d: -f2 | sed s/kB//`                 # total memory without kB
        system_memory_free=`cat /proc/meminfo | grep MemFree | cut -d: -f2 | sed s/kB//`                   # fecth free memory
        system_memory=`expr $system_memory_total - $system_memory_free`                                    # compute memory in use
        echo "$mytime    $falcon_memory    $system_memory    $hua_memory    $piculet_memory" >> $logfile   # adds all 5 above into the log file
        sed -i "s/[kK][bB]//g" $logfile
        mydate=`date +%m%d%Y`
        do_get_cpu $mydate $mytime
        sleep $1
        lines=`cat $logfile | wc -l`        # checks number of lines in the cpu log file memory_check.log
        cpulines=`cat $logfileCpu | wc -l`  # checks number of lines in the memory_check.csv cpu

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

