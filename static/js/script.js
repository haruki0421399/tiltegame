let requestURL = '../static/js/sample.json';
let request = new XMLHttpRequest();
request.open('GET', requestURL);

request.responseType = 'json';
request.send();

// request.onload = function() {
//     const data = request.response;
//     //console.log(data[2])
//   }

  const data = request.response;
  console.log(data)

  function buttonClick(){
    alert("jjjj");
}