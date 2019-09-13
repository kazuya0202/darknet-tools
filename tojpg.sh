: <<*
	ファイル名一括変更（連番
*

SAVEIFS=$IFS
IFS=$'\n' # ファイル名の区切りを改行にする
count=0   # 連番
target_dir='seqren-images'

if [ -n "$1" ]; then
	target_dir="$1"
fi

count=0
# 変更する拡張子
declare -a extensions=(
	"*.png"
	"*.PNG"
	"*.jpeg"
	"*.JPEG"
	"*.gif"
	"*.GIF"
	"*.tif"
	"*.TIF"
	"*.tiff"
	"*.TIFF"
)

# extensionsの要素がある間
for ex in ${extensions[@]}; do
	# カレントディレクトリだけ
	for file in $(find "./${target_dir}" -maxdepth 1 -type f -name "${ex}"); do
		fname=$(basename $file | sed 's/\.[^\.]*$//')
		ffmpeg -i $file -vcodec copy -threads 4 "${target_dir}/${fname}.jpg" -y && rm $file
	done
done

# JPG to jpg
for file in $(find "./${target_dir}" -maxdepth 1 -type f -name "*.JPG"); do
	# 大文字をすべて小文字に
	new=$(echo $file | tr '[:upper:]' '[:lower:]')
	mv "$file" "$new"
done

IFS=$SAVEIFS
