var degree,branch,section;
var current_class;

var period=document.getElementsByClassName('period_order')

function create_class(){
    const degree  = document.getElementById("degree").value;
  const branch  = document.getElementById("branch").value;
  const section = document.getElementById("section").value;

  fetch("/attendo/faculty/addclass/", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken' : getCookie('csrftoken')
      },
      body: JSON.stringify({ degree, branch, section })
  })
  .then(res => res.json())
  .then(data => {
    if (data.status === 'success') {
      window.location.href = `/attendo/faculty/studentlist/${data.class_id}/`;
    } else {
      alert("Could not create class");
    }
  })
}







function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function add_student(class_id){
  console.log(class_id)
  const name=document.getElementById("name").value
  const regno=document.getElementById("regno").value
  const stu_username=document.getElementById('stu_username').value
  fetch(`/attendo/faculty/studentlist/${class_id}/addstu`,
    {
      method:'POST',
      headers:{
        'Content-Type':'application/json',
        'X-CSRFToken' : getCookie('csrftoken')
      },
      body:JSON.stringify({name,regno,stu_username})
    }).then(response=>response.json())
    .then(data => {
      if (data.status === 'success') {
        window.location.href = `/attendo/faculty/studentlist/${data.class_id}/`;
      } else {
        alert("Could not create class");
      }
    })
}


function delete_class(class_id){

  fetch('/attendo/faculty/home',
    {method:'POST',
     headers:{
      'Content-Type':'application/json',
      "X-CSRFToken":getCookie('csrftoken')
     } ,
     body:JSON.stringify({class_id})
    }
  ).then(res=>res.json())
  .then(data =>{
    if(data.status==='success'){
      window.location.href = `/attendo/faculty/home`;
    }else{
      alert("Error")
    }
  })
}



function delete_student(student_id,class_id){
  console.log("he")
  fetch(`/attendo/faculty/studentlist/${class_id}/`,
    {
      method:"POST",
      headers:{
        'Content-Type':"application/json",
        "X-CSRFToken":getCookie('csrftoken')
      },
      body:JSON.stringify({student_id})
    }
  ).then(res=>res.json())
  .then(data=>{
    if(data.status==="success"){
      window.location.href=`/attendo/faculty/studentlist/${class_id}/`;
    }
    else{alert('Error')}
  })
}