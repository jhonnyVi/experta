  #!/bin/bash 
limpio=''
rm -r filelimpioPaises.txt
rm -r filelimpiolistaNegra.txt

limpiar() {
    limpio=`echo "$1" | tr '[:upper:]' '[:lower:]'`;
    limpio=`echo "${limpio//á/a}"`;
    limpio=`echo "${limpio//é/e}"`;
    limpio=`echo "${limpio//í/i}"`;
    limpio=`echo "${limpio//ó/o}"`;
    limpio=`echo "${limpio//ú/u}"`;
    limpio=`echo "${limpio//ñ/n}"`;
} 



while read line; do
	limpiar "$line" 
	echo "$limpio" >> filelimpiolistaNegra.txt ; 
done < $2

while read line; do
	limpiar "$line"
	v=`cat filelimpiolistaNegra.txt | grep -c  "$limpio"`;
	if [ $v -lt 1  ];
	then 
		python3 __init__.py "$line"
	fi
done < $1


