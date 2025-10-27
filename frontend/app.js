Dropzone.autoDiscover = false;

function init() {
    let dz = new Dropzone("#dropzone", {
        url: "#",
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false
    });
    
    dz.on("addedfile", function() {
        if (dz.files[1]!=null) {
            dz.removeFile(dz.files[0]);        
        }
    });

    dz.on("complete", function (file) {

        //var url = "http://127.0.0.1:5000/classify_image"; // Use this if you are NOT using nginx
        var url = "/api/classify_image";
        $.post(url, {
            image_data: file.dataURL
        },function(data, status) {
            //console.log(data);
            if (!data || data.length==0) {
                $("#resultHolder").hide();
                $("#divClassTable").hide();                
                $("#error").show();
                return;
            }

            let match = [];
            let bestScore = -1;
            console.log(data)
            for (let i=0;i<data.length;++i) {
                let maxScoreForThisClass = Math.max(...data[i].class_probability);
                console.log(maxScoreForThisClass)

                if(maxScoreForThisClass>bestScore && maxScoreForThisClass > 40) {
                    match.push(data[i]);
                    //bestScore = maxScoreForThisClass;
                }
            }
            console.log('ok@@@@')
            console.log(match)
            console.log('ok@@@@')

            if (match.length>0) {
                $("#error").hide();
                $("#resultHolder").show();
                $("#divClassTable").show();
                const $container = $("#resultHolder").empty();
                let classDictionary = '';
                let class_probability = []
                for (i =0; i<match.length; ++i) {
                    $container.append($(`[data-player="${match[i].class}"`).html());
                    classDictionary = match[i].class_dictionary;
                    if (class_probability.length==0) {
                        class_probability.push(match[i].class_probability)
                    } else {
                        max_val = Math.max(...match[i].class_probability)
                        let max_index = match[i].class_probability.indexOf(max_val);
                        console.log(max_index)
                        class_probability[0][max_index] = max_val
                    }
                }
                console.log('*********')
                console.log(classDictionary)
                console.log(class_probability)
                console.log('*********')
                // if (match.length>1) {
                //     console.log(match)
                // } else {
                //
                // }

                for(let personName in classDictionary) {
                    let index = classDictionary[personName];
                    let proabilityScore = class_probability[0][index];
                    let elementName = "#score_" + personName;
                    $(elementName).html(proabilityScore);
                }
            } else {
                $("#resultHolder").hide();
                $("#divClassTable").hide();
                $("#error").show();
            }
            // dz.removeFile(file);            
        });
    });

    $("#submitBtn").on('click', function (e) {
        dz.processQueue();		
    });
}

$(document).ready(function() {
    console.log( "ready!" );
    $("#error").hide();
    $("#resultHolder").hide();
    $("#divClassTable").hide();

    init();
});