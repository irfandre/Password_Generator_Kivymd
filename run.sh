#! /bin/bash/


send_file () {
    for f in {1..19}
    do
            echo "Processing $f file..."
            #if wget --spider http://192.168.1.$f:8181 2>/dev/null; then
            #curl -Is http://192.168.1.$f:8181/ | head -n 1
            res=$(curl -sL -w "%{http_code}\\n" "http://192.168.1.$f:8181/" -o /dev/null --connect-timeout 1)
            if [ $res == 200 ]; then
                echo "Server found at host: $f"
                host_id=$f
                break
            fi
            if [ $f == 19 ]; then
                echo 'Server not running'
                read -p $'\e[31mPlease turn on server in phone and Press ENTER to try Again / type No to exit: \e[0m' uservar
                #counter=$1
                while [ "$uservar" == "" ]
                do
                    send_file
                done
                # break

            fi
    done
    echo $host_id
}
# read -p 'Press enter to continue: ' uservar
cmd=$(buildozer -v android debug | tail -2 | awk NF)
# cmd=`printf "one.apk\ntwo\nthree one two three "`
#cmd=`printf "# APK password_generator-0.1-armeabi-v7a-debug.apk available in the bin directory"`
apk=$(printf "${cmd}" | cut -d ' ' -f 3)

if [[ $apk == *".apk"* ]]; then
    printf "\nFound apk: ${apk}\n"
   echo "uploading the newly generated apk $apk !"
   send_file
else
   echo 'not apk'
fi
