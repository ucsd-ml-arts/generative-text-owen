# CHANGE ME
IMAGE_PATH=/home/owen/workspace/visual-questioner/images/water.jpg

function parse_yaml {
    # Source: https://stackoverflow.com/a/21189044.
    local prefix=$2
    local s='[[:space:]]*' w='[a-zA-Z0-9_]*' fs=$(echo @|tr @ '\034')
    sed -ne "s|^\($s\):|\1|" \
        -e "s|^\($s\)\($w\)$s:$s[\"']\(.*\)[\"']$s\$|\1$fs\2$fs\3|p" \
        -e "s|^\($s\)\($w\)$s:$s\(.*\)$s\$|\1$fs\2$fs\3|p"  $1 |
    awk -F$fs '{
        indent = length($1)/2;
        vname[indent] = $2;
        for (i in vname) {if (i > indent) {delete vname[i]}}
        if (length($3) > 0) {
            vn=""; for (i=0; i<indent; i++) {vn=(vn)(vname[i])("_")}
            printf("%s%s%s=\"%s\"\n", "'$prefix'",vn, $2, $3);
        }
    }'
}
eval $(parse_yaml config.yaml)
CHECKPOINT_PATH="${project_root_dir}/${checkpoint_path}"
VOCAB_FILE_PATH="${project_root_dir}/${vocab_file_path}"

cd vtensorflow/models/research/im2txt
python3 im2txt/run_inference.py --checkpoint_path=${CHECKPOINT_PATH} --vocab_file=${VOCAB_FILE_PATH} --input_files=${IMAGE_PATH}
