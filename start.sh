#!/bin/bash

#选择执行测试用例的级别
#caseLevel="highs"
caseLevel='temp_caseLevel'
#获取当前pod的名称
podname=$(echo $POD_NAME|awk -F "-" '{print $8}')
#podname='podabc'
#根据当前节点名称、pod名称以及UUID，拼接一个名称，用作后续pod容器名称
uuid=$(cat /proc/sys/kernel/random/uuid|md5sum|cut -c 1-9)
#podtestdatafoldername="k8s-node1-"${podname}'-'$uuid
podtestdatafoldername=${NODE_NAME}"-"${podname}'-'$uuid

#所有本次跑的pod，都会将测试数据放在该目录下
#testdatafoldername='2022-11-22-11-39-29'
testdatafoldername='temp_build_id'

#这个是共享文件夹的路径，所有测试数据，都会放在这个目录下
testpath='/uitestdemotestdata/'

projectName='temp_job_name'

#本次跑的allure测试数据，都会在该目录下
podtestresultpath=${testpath}${projectName}'/'${testdatafoldername}'/'${podtestdatafoldername}'/result'

#本次构建，所有的pod的allure测试数据，均会放在该目录下
testprojectresultpath=${testpath}${projectName}'/'${testdatafoldername}'/result/'
#本次构建，allure的测试报告
testprojectreportpath=${testpath}${projectName}'/'${testdatafoldername}'/report/'

#创建相关的文件
echo $podtestresultpath
mkdir -p $podtestresultpath
mkdir -p $testprojectresultpath
mkdir -p $testprojectreportpath

#当前脚本的路径
currentPath=$(pwd)
#测试脚本的路径
casesPath=$currentPath"/cases/"

#替换cases文件夹下所有的测试类的名称，在测试类的名称后面加上pod的名称
replaceCaseClassname(){
   #获取cases路径下的所有测试用例中的文件，并且文件以test_*.py格式
   files=$(find $casesPath -type f -name "test_*.py")
   for file in $files;do
      #获取每个test_*.py文件中的类名，并且类名是以Test_开头
      classNames=$(cat $file |awk '/class /{split($2,arr,":");print arr[1]}')
      for className in $classNames;do
         targetClassname=${className}"_"$podname
         targetClassnameLength=$(expr length $targetClassname)
         echo "replaceCaseClassname function---------------targetClassname---------"$targetClassname
         #podname的长度是5，加上测试类名是以Test_开头，长度也为5，加起来为10
         if [ $targetClassnameLength -gt 10 ] && [ ${targetClassname: 0: 5} == "Test_" ];then
           tempClassName=${className}":"
           tempTargetClassname=${targetClassname}":"
           sed -i s#$tempClassName#$tempTargetClassname#g $file
         fi
      done
      echo "replaceCaseClassname function----the source file "$file" and the point classNames is "$classNames
   done
}

runTestcase(){
   echo "runTestcase--------current caselevel is "$caseLevel
   if [ $caseLevel == "highs" ] || [ $caseLevel == "lows" ];then
      pytest -v -m $caseLevel -s . --alluredir $podtestresultpath --clean-alluredir
   elif [ $caseLevel == "all" ];then
      pytest -v -s . --alluredir $podtestresultpath --clean-alluredir
   else
      echo "runTestcase funciton-----------the caselevel param is error,and the param is "$caseLevel
   fi
   cp -r $podtestresultpath'/.' $testprojectresultpath
}
run(){
   replaceCaseClassname
   runTestcase
}
run
exit 0
