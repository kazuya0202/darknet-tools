<< COM
	ファイル名一括変更（連番
COM

SAVEIFS=$IFS
IFS=$'\n'	# ファイル名の区切りを改行にする
count=0	# 連番
target_dir='seqrename-images'

# 一度他と被らないようなランダムな文字で全ファイルをリネーム
# ファイル名が同じで拡張子だけが違う場合にファイルが消る可能性があるため
for file in `find "./${target_dir}" -maxdepth 1 -type f -name "*"`; do
	count=$(expr $count + 1)	# インクリメント
	fname="EX9brx6MAZN`printf %03d ${count}`"	# 0埋め3桁 / 連結
	ex=`echo $file | sed 's/^.*\.\([^\.]*\)$/\1/'`

	if [ "${file}" != "${fname}.${ex}" ]; then
		# ファイル名変更
		mv $file "${target_dir}/${fname}.${ex}"
	fi
done

count=0
declare -a extensions=(	# 変更する拡張子
	"*.png"
	"*.PNG"
	"*.jpeg"
	"*.JPEG"
	"*.gif"
	"*.GIF"
)

# extensionsの要素がある間
for ex in ${extensions[@]}; do
	# カレントディレクトリだけ
	for file in `find "./${target_dir}" -maxdepth 1 -type f -name "${ex}"`; do
		fname=`basename $file | sed 's/\.[^\.]*$//'`
		./bin/ffmpeg.exe -i $file -vcodec copy -threads 4 "${target_dir}/${fname}.jpg" -y && rm $file
	done
done

# JPG to jpg
for file in `find "./${target_dir}" -maxdepth 1 -type f -name "*.JPG"`; do
	# 大文字をすべて小文字に
	new=`echo $file | tr '[:upper:]' '[:lower:]'`
	mv "$file" "$new"
done



# 入力
[ $1 ] && name=$1 || read -p "> Enter new file name: " name

for file in `find "./${target_dir}" -maxdepth 1 -type f -name "*.jpg"`; do
	count=$(expr $count + 1)	# インクリメント
	fname="${name}`printf %03d ${count}`"	# 0埋め3桁 / 連結

	mv $file "${target_dir}/${fname}.jpg"	# ファイル名変更
done


echo -e "\n** finished renaming."	# message

IFS=$SAVEIFS

