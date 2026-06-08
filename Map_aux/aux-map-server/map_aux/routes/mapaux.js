var express = require('express');
var router = express.Router();

/* GET map page. */
router.get('/',async function(req, res, next) {
  const response = await fetchMapdata();
  res.json(response);
});

module.exports = router;

async function fetchMapdata() {
    try{
        const response = await fetch(`http://localhost:5000/api/jobs`);
      if(!response.ok){
        throw new Error(`Response status {response.status}`);
      }
        const result = await response.json();
        console.log(result);

        temp = parseJobData(result);
        console.log(temp);
        
        //temp = JSON(temp);
        console.log(typeof(temp)+"fetchmapdata ends");
        
        return temp;
        //document.getElementById("test_box").innerHTML = JSON.stringify(temp);

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


