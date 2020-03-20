///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/////       Owner book search results table display
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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
    cell.innerHTML= value.link('/OwnerDetails')
    }
    else if (key=='image_url'){
        var img= document.createElement('img');
        img.src= value;
        cell.appendChild(img); 
            }
 
    else {
        cell.innerHTML= value
    }
    })
})
}

//create bookresults table--- display results when owner is searching for the books and adding details
var url2 = "/api/findbook_owner";
d3.json(url2).then(function(response) {

    console.log(response);
    
    var table = document.getElementById("get-books");
    var data = Object.keys(response[0]);

    generateTableHead(table, data);     //call function to generate table
    generateTable(table, response);     //call fucntion to add table header
   
        //select book results to redirect to enter owner details
    var book_table=d3.select('#get-books')
    book_table.selectAll('td').on('click', function(){
        
        var title= d3.select(this).text()
        var form_title=d3.getElementById('#inputTitle')
        var form=document.getElementById('form')


        console.log(this)
        console.log(form_title)
        form_title.innerHTML=`"${title}"`
/*         url2= `/api/findSharedBook/${title}`
        d3.json(url3).then(function(datasheet){

            console.log(datasheet) */
        })
});
