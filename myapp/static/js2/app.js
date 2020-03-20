//function to create table header for search results
function generateTableHead(table, data) {
    var thead = table.createTHead();
    var row = thead.insertRow();
    data.forEach((key)=> {
        var cell = row.insertCell();
        cell.innerHTML= key;
    })
  }
  
//function to create table rows for search results
function generateTable(table, data) {

data.forEach((element)=> {
    var row = table.insertRow();
    Object.entries(element).forEach(([key,value])=> { 
    
        // console.log(`element print ${key}----${value}`)    

    var cell = row.insertCell();

    if (key=='Title'){
    cell.innerHTML= value
    }
    else if (key=='image_url'){
        var img= document.createElement('img');
        img.src= value;
        cell.appendChild(img); 
            }
 
    else if (key=='id'){
        cell.innerHTML= value
    }
    })
})
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////       uSer book search results table display
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//create bookresults table--- display results when user is searching for the books
var url = "/api/findbook";
d3.json(url).then(function(response) {

    console.log(response);
    
    var table = document.getElementById("get-books");
    var data = Object.keys(response[0]);
    
    generateTableHead(table, data);         //call fucntion to add table header
    generateTable(table, response);         //call function to generate table
   
    var id_table=d3.select('#get-books')
    id_table.selectAll('td').on('click', function(){
        var id= d3.select(this).text()
        console.log(this)
        url3= `/api/findSharedBook/${id}`
        d3.json(url3).then(function(datasheet){
            
            console.log(datasheet);
            var table = document.getElementById("get-books");
            table.innerHTML=''
             
            datasheet.forEach((element)=> {
                var row = table.insertRow();
                Object.entries(element).forEach(([key,value])=> { 
                
                    // console.log(`element print ${key}----${value}`)    
                if (key=='Owners'){
                    var owner = Object.keys(value[0]);
                    generateTableHead(table, owner);         //call fucntion to add table header
                    
                    value.forEach((element)=> {
                        var row = table.insertRow();
                        Object.entries(element).forEach(([key,value])=> { 
                            var cell = row.insertCell();
                            cell.innerHTML=value;

                            
                        })
                    })                    
                }
                
            });
        });
    });
    
});
});


    /* onClick{
        var title= this.value
        


    } */


  

//select book results to redirect to display owner details and Locations

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////       Owner book search results table display
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//create bookresults table--- display results when owner is searching for the books and adding details
// var url2 = "/api/findbook_owner";
// d3.json(url2).then(function(response) {

//     console.log(response);
    
//     var table = document.getElementById("get-books");
//     var data = Object.keys(response[0]);

//     generateTableHead(table, data);     //call function to generate table
//     generateTable(table, response);     //call fucntion to add table header
    
   
// });

//select book results to redirect to enter owner details