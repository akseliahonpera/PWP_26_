

async function fetchMapdata() {
    try{
        const response = await axios.get(`http://localhost:5000/api/jobs`);

        temp = parseJobData(response.data);


        document.getElementById("test_box").innerHTML = JSON.stringify(temp);

    }catch(error){
        console.error(`Error fetching job data:`, error.message);
        throw new Error('Map service effed up.');
    }
}


function parseJobData(data){

    var parsedJobData= [];
    for(let i=0; i<data.length; i++){
        varJson = null;
        
        varJson= {"job_name": data[i]["job_name"],
                  "longitude": data[i]["longitude"],
                  "latitude":data[i]["latitude"],
                  "category": data[i]["category"]
        };

        parsedJobData.push(varJson);
    }
    return parsedJobData;
}


fetchMapdata();