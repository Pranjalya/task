FILEPATH=sounds/samples/vi95kMQ65UeU7K1wae12D1GUeXd2

for i in $(ls $FILEPATH); do
    file=$FILEPATH'/'$i
    echo "Peaks occur for file $i at following seconds : "
    peaks=$(curl --no-progress-meter -X POST -F file=@$file https://cough-detector.herokuapp.com/detect_coughs | jq -r '.peak_start' | jq -r .[])
    if [[ -z "$peaks" ]]
    then
        echo "The audio file does not contain any coughs"
    else
        echo $peaks
    fi
    echo
done
