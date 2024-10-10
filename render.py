def html_content():
    return """
<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <title>A L P H A</title>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Quicksand&display=swap">
  
  <style>
@font-face {
  font-family: "CastoroTitling";
  src: url("https://s3.us-east-2.amazonaws.com/cdn.spotlessplace.com/wp-content/CastoroTitling-Regular.ttf")
    format("truetype");
}

@font-face {
  font-family: BraahOne;
  src: url("https://s3.us-east-2.amazonaws.com/cdn.spotlessplace.com/wp-content/Merriweather-Regular.ttf");
}

body {
  margin: 0;
  font-family: 'Quicksand', sans-serif;
  font-size: 12px;
  overflow: hidden;
}
@keyframes zoom {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}
#backgroundimg {
  object-fit: cover;
  object-position: center center;
  width: 100%;
  height: 100%;
  position: fixed;
  z-index: -1;
  animation: zoom 20s infinite alternate;
}

.main {
  background-color: rgba(255, 255, 255, 0.04);
  height: 625px;
  width: 450px;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  border-radius: 30px;
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  overflow: hidden;
  transition: transform 1s ease, width 1s ease;
}

.header {
  color: #fff;
  display: flex;
  padding: 20px;
  align-items: center;
}

#pfpname {
  margin-left: 20px;
  display: inline-block;
  font-size: 25px;
  transition: letter-spacing 0.3s ease;
}

.notifications {
  background: #2796db;
  border-radius: 100%;
  aspect-ratio: 1;
  width: 25px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-left: 5px;
  cursor: pointer;
  transition: transform 2s ease;
}
.notifications:hover {
  transition: transform 2s ease;
}
.header .pfp {
  height: 60px;
  width: 60px;
  border-radius: 100%;
  cursor: pointer;
  transition: transform 1s ease;
}

.header .center {
  display: flex;
  justify-content: center;
  text-align: center;
  width: 100%;
}

.header .center div p {
  margin: 0;
  font-weight: 700;
}

.footer {
  width: 100%;
  height: 100px;
  position: fixed;
  bottom: -8px;
  display: inline-flex;
  align-items: center;
}

.text-box {
  float: right;
  border-radius: 100px;
  border: 1px solid rgba(255, 255, 255, 0.6);
  background: none;
  padding: 8px 10px;
  width: 400px;
  height: 30px;
  padding-left: 20px;
  outline: none;
  color: #fff;
  transition: transform 1s ease, width 1s ease;
}

.send-ico {
  height: 10px;
  width: 10px;
  color: #fff;
  position: absolute;
  right: 0;
  background: #2796db;
  border-radius: 100%;
  margin-right: 15px;
  margin-top: 6px;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 13px;
  cursor: pointer;
}

.text-box::placeholder {
  color: #c6c6c6;
  font-family: BraahOne;
}

.content {
  width: 100%;
  bottom: 82px;
  position: absolute;
  height: 440px;
  text-align: center;
  color: #afafaf;
  overflow: auto;
  border-radius: 15px;
  border-top: 1px solid rgba(255, 255, 255, 0.3);
}

.content::-webkit-scrollbar {
  width: 8px; /* Adjust the width as per your preference */
}

.content::-webkit-scrollbar-track {
  background-color: transparent; /* Make the track transparent */
}

.content::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.content::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.3); /* Change the thumb color on hover */
}
    
.msg-btn {
  color: #fff;
  word-wrap: break-word;
  text-align: left;
  border-radius: 20px;
  display: inline-block;
  max-width: 80%;
  font-size: 16px;
  font-family: 'Quicksand', sans-serif;
  margin-bottom: 10px;
}
.msg-btn p {
  padding: 10px 15px;
  margin: 0;
}
.msg-btn-holder {
  padding-bottom: 30px;
  width: 100%;
  margin-top: 10px;
}
.receiver-msg {
  background: #4c4c4c;
  float: left;
}
.sender-msg {
  background: #2798fc;
  float: right;
}


.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 10px;
  border-radius: 5px;
  opacity: 0;
  transition: opacity 0.5s;
}

.hidden {
  display: none;
}

.custom-menu {
  position: absolute;
  background-color: #333333;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.15);
  padding: 20px;
  font-family: Arial, sans-serif;
  font-size: 14px;
  color: #ffffff;
  border-radius: 4px;
  max-width: 300px;
  z-index: 9999;
}

.custom-menu div {
  margin-bottom: 8px;
}

.custom-menu label {
  margin-right: 5px;
  font-size: 17px;
}

.custom-menu input {
  background: rgba(0,0,0,0);
  border: none;
  color: #fff;
  margin-bottom: 5px;
  font-size: 15px;
}

.custom-menu input:focus {
  outline: none;
}

.custom-menu button {
  background-color: #ff0000;
  color: #ffffff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  display: block;
  margin: 0 auto;
  margin-top: 20px;
}

.custom-menu button:hover {
  background-color: #cc0000;
}

.arrow {
    height: 25px;
    width: 25px;
    background-color: #333333;
    transform: rotate(45deg);
}

.preview {
    height: 60px;
    aspect-ratio: 1;
    object-fit: cover;
    border-radius: 50%;
    margin-top: auto;
    margin-bottom: auto;
    margin-left: 9px;
    box-shadow: 0 0 5px 1px #ffffff29;
}


.preview:hover {
    position: absolute;
    border-radius: 20px;
    aspect-ratio: auto;
    height: 200px;
}


.dropdown {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 0 20px;
  width: 340px;
}

.dropdown-item {
  margin-bottom: 10px;
}

.dropdown-title {
  cursor: pointer;
    font-weight: bold;
    margin-bottom: 5px;
    display: inline-block;
    max-width: 280px;
    overflow: hidden;
    font-family: 'Quicksand';
    text-overflow: ellipsis;
}

.dropdown-details {
  display: none;
  list-style: none;
  padding-left: 15px;
  max-width: 280px;
}

.detail-item {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.detail-text {
  display: flex;
  flex-direction: column;
  margin-right: 10px;
}

.detail-image img {
  width: 60px;
  height: 80px;
  object-fit: cover;
  border-radius: 5px;
}

.dropdown-item:hover .dropdown-details {
  display: block;
}


@keyframes rotate {
  from {
    rotate: 0deg;
  }

  50% {
    scale: 1 1.5;
  }

  to {
    rotate: 360deg;
  }
}

  </style>
</head>
<body>
<link rel="stylesheet" href="https://site-assets.fontawesome.com/releases/v6.2.1/css/all.css" crossorigin="anonymous" referrerpolicy="no-referrer" />

<img id="backgroundimg" src="https://cdn.pixabay.com/photo/2016/11/29/04/42/conifers-1867371_960_720.jpg">
<div class="main">
  <div class="header">
    <div class="center">
      <div style="line-height: 60px;display: flex;">
        <img class="pfp" src="https://i.ibb.co/kXJ7z1g/logo.png">
        <p id="pfpname">A L P H A <sub>(beta)</sub></p>
      </div>

    </div>

  </div>

  <div class="content">
    <div style="padding:11px;">

      <svg id="pageLoading" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="margin-right: auto; margin-left: auto; margin-top: 105px; background: rgba(221, 221, 221, 0); display: block;" width="200px" height="200px" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
<g transform="translate(50,50)"><circle cx="0" cy="0" r="8.333333333333334" fill="none" stroke="rgba(265,265,265,0.1)" stroke-width="4" stroke-dasharray="26.179938779914945 26.179938779914945">
<animateTransform attributeName="transform" type="rotate" values="0 0 0;360 0 0" times="0;1" dur="1s" calcMode="spline" keySplines="0.2 0 0.8 1" begin="0" repeatCount="indefinite"></animateTransform>
</circle><circle cx="0" cy="0" r="16.666666666666668" fill="none" stroke="rgba(265,265,265,0.1)" stroke-width="4" stroke-dasharray="52.35987755982989 52.35987755982989">
<animateTransform attributeName="transform" type="rotate" values="0 0 0;360 0 0" times="0;1" dur="1s" calcMode="spline" keySplines="0.2 0 0.8 1" begin="-0.2" repeatCount="indefinite"></animateTransform>
</circle><circle cx="0" cy="0" r="25" fill="none" stroke="rgba(265,265,265,0.1)" stroke-width="4" stroke-dasharray="78.53981633974483 78.53981633974483">
<animateTransform attributeName="transform" type="rotate" values="0 0 0;360 0 0" times="0;1" dur="1s" calcMode="spline" keySplines="0.2 0 0.8 1" begin="-0.4" repeatCount="indefinite"></animateTransform>
</circle><circle cx="0" cy="0" r="33.333333333333336" fill="none" stroke="rgba(265,265,265,0.1)" stroke-width="4" stroke-dasharray="104.71975511965978 104.71975511965978">
<animateTransform attributeName="transform" type="rotate" values="0 0 0;360 0 0" times="0;1" dur="1s" calcMode="spline" keySplines="0.2 0 0.8 1" begin="-0.6" repeatCount="indefinite"></animateTransform>
</circle><circle cx="0" cy="0" r="41.666666666666664" fill="none" stroke="rgba(265,265,265,0.1)" stroke-width="4" stroke-dasharray="130.89969389957471 130.89969389957471">
<animateTransform attributeName="transform" type="rotate" values="0 0 0;360 0 0" times="0;1" dur="1s" calcMode="spline" keySplines="0.2 0 0.8 1" begin="-0.8" repeatCount="indefinite"></animateTransform>
</circle></g>
</svg>
      
    </div>

  </div>
  <div class="footer">
    <div style="width:100%;padding:11px;">
      <form id="send">
      <input placeholder="Message" class="text-box" name="message" required>
      <div class="send-ico">
        <i style="position:absolute;" class="fas fa-paper-plane"></i>
      </div>
      </form>
    </div>

  </div>

<div id="popup" class="popup hidden">Social searches may take a few seconds, please hold back.</div>

<script>

// Get the form element by its ID
var form = document.getElementById('send');
window.loading = true;
  
window.onload = function() {
  setTimeout(function() {
      var pageLoadingElement = document.getElementById("pageLoading");
      if (pageLoadingElement) {
        pageLoadingElement.parentNode.removeChild(pageLoadingElement);
      }
      var contentDiv = document.querySelector('.content div:first-child');
      // Create the receiver message element with the animation
      var receiverMsgElement = document.createElement('div');
      receiverMsgElement.className = 'receiver-msg msg-btn';
      receiverMsgElement.innerHTML = '<p style="font-size: 20px;">.</p>';
    
      // Append the receiver message element to the first div within the div with class "content"
      contentDiv.appendChild(receiverMsgElement);
    
      // Animate the dots
      var dotsAnimation = setInterval(function() {
        var dots = receiverMsgElement.querySelector('p');
        dots.textContent += ' .';
        if (dots.textContent.length > 5) {
          dots.textContent = '.';
        }
      }, 500); // Change the delay (in milliseconds) for the desired animation speed
      setTimeout(function() {
          clearInterval(dotsAnimation);
          receiverMsgElement.parentNode.removeChild(receiverMsgElement);
          // Create the receiver message element with the received text
          var newReceiverMsgElement = document.createElement('div');
          newReceiverMsgElement.className = 'msg-btn-holder';
          newReceiverMsgElement.innerHTML = `
            <div class="receiver-msg msg-btn">
              <p>Hello sir! How may I assist you today?</p>
            </div>
          `;
  
          // Append the new receiver message element to the first div within the div with class "content"
          contentDiv.appendChild(newReceiverMsgElement);
        window.loading = false;
      }, 2000);
  }, 1000);
};

// Add an event listener for form submission
form.addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent the form from submitting normally

  if(window.loading) {
    return
  }
  
  window.loading = true;

  // Get the input value
  var inputValue = document.querySelector('#send input').value;
  checkfuck(inputValue)
  // Create the sender message element
  var senderMsgElement = document.createElement('div');
  senderMsgElement.className = 'msg-btn-holder';
  senderMsgElement.innerHTML = `
    <div class="sender-msg msg-btn">
      <p>${inputValue}</p>
    </div>
  `;

  // Append the sender message element to the first div with class "content"
  var contentDiv = document.querySelector('.content div:first-child');
  document.querySelector('#send input').value = "";
  contentDiv.appendChild(senderMsgElement);

  // Create the receiver message element with the animation
  var receiverMsgElement = document.createElement('div');
  receiverMsgElement.className = 'receiver-msg msg-btn';
  receiverMsgElement.innerHTML = '<p style="font-size: 20px;">.</p>';
  
  // Append the receiver message element to the first div within the div with class "content"
  contentDiv.appendChild(receiverMsgElement);
  scrollToBottom(document.querySelector('.content'));

  // Animate the dots
  var dotsAnimation = setInterval(function() {
    var dots = receiverMsgElement.querySelector('p');
    dots.textContent += ' .';
    if (dots.textContent.length > 5) {
      dots.textContent = '.';
    }
  }, 500); // Change the delay (in milliseconds) for the desired animation speed

  scrollToBottom(document.querySelector('.content'));
  // Send the data to "/process" using POST request
  var xhr = new XMLHttpRequest();
  xhr.open('POST', 'http://127.0.0.1:5000/process', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {

      // Remove the dots element
      setTimeout(function() {
        
        // Clear the dots animation interval
        clearInterval(dotsAnimation);
        receiverMsgElement.parentNode.removeChild(receiverMsgElement);

        if (xhr.status === 200) {
          // Get the response text
          var responseText = JSON.parse(xhr.responseText);
  
          // Create the receiver message element with the received text
          var newReceiverMsgElement = document.createElement('div');
          newReceiverMsgElement.className = 'msg-btn-holder';
          newReceiverMsgElement.innerHTML = `
            <div class="receiver-msg msg-btn" intents='${responseText.intents}' entities='${responseText.entities}'>
              <p>${responseText.text}</p>
            </div>
          `;
  
          // Append the new receiver message element to the first div within the div with class "content"
          contentDiv.appendChild(newReceiverMsgElement);
          scrollToBottom(document.querySelector('.content'));
          window.loading = false;
        } else {
          // Handle the case when the request fails
          console.error('Request failed with status:', xhr.status);
          window.loading = false;
          // Create the receiver message element with the received text
          var newReceiverMsgElement = document.createElement('div');
          newReceiverMsgElement.className = 'msg-btn-holder';
          newReceiverMsgElement.innerHTML = `
            <div class="receiver-msg msg-btn" intents="['error']" entities="['error']">
              <p style="color:orange;">ALPHA encountered an error while processing your request, check logs for more info or try again.</p>
            </div>
          `;
  
          // Append the new receiver message element to the first div within the div with class "content"
          contentDiv.appendChild(newReceiverMsgElement);
          scrollToBottom(document.querySelector('.content'));
        }

      
      }, 2000)

      
    }
  };

  // Send the request with the input value as data
  xhr.send('input=' + encodeURIComponent(inputValue));
});

// Function to scroll to the bottom of an element
function scrollToBottom(element) {
  element.scrollTop = element.scrollHeight;
}


document.getElementsByTagName('input')[0].addEventListener('keyup', function(event) {
      if (event.key === 'ArrowUp') {
        var senderMsgs = document.querySelectorAll('.content .sender-msg');
        if (senderMsgs.length > 0) {
          var lastMsg = senderMsgs[senderMsgs.length - 1];
          var text = lastMsg.querySelector('p').textContent;
          document.getElementsByTagName('input')[0].value = text;
        }
      }
    });

var fuck = ["instagram", "insta", "facebook", "fb"]
  function checkfuck(sentence){
    const regex = /^find\s+((?:\w+\s+)*\w+)\s+on\s+(\w+)$/i;
    const match = sentence.match(regex);
    
    if (match) {
      const a = match[1].split(/\s+/); 
      const b = match[2];
      if(fuck.includes(b)){
        showPopup();
      }
    }
  }
  function showPopup() {
    const popup = document.getElementById('popup');
    popup.classList.remove('hidden');
    setTimeout(() => {
      popup.style.opacity = '1';
    }, 100);
    setTimeout(() => {
      hidePopup();
    }, 2500);
  }
  
  function hidePopup() {
    const popup = document.getElementById('popup');
    popup.style.opacity = '0';
    setTimeout(() => {
      popup.classList.add('hidden');
    }, 500);
  }
  
// Add an event listener to the document to detect right-clicks on elements with class "receiver-msg"
document.addEventListener("contextmenu", function(event) {
    let menu = document.querySelector(".custom-menu");
    if(menu) {
        menu.remove();
	document.querySelector(".arrow");
    }
    var targetElement = event.target.parentNode;
    if (targetElement.classList.contains("receiver-msg")) {
        event.preventDefault(); // Prevent the default right-click menu from appearing

        // Get the relevant information from the target element and its previous sibling
        var intents = targetElement.getAttribute("intents");
        var entities = targetElement.getAttribute("entities");
        var promptText = targetElement.parentNode.previousSibling.innerText;
	
	// Create the arrow of the right menu
	var arrow = document.createElement("div")
	arrow.classList.add("arrow");
	document.body.appendChild(arrow)

        // Create a custom right-click menu
        var contextMenu = document.createElement("div");
        contextMenu.classList.add("custom-menu");

        // Create the intents input field
        var intentsLabel = document.createElement("label");
        intentsLabel.textContent = "Intents:";
        contextMenu.appendChild(intentsLabel);

        var intentsInput = document.createElement("input");
        intentsInput.type = "text";
        intentsInput.value = intents;
        intentsInput.addEventListener("click", function(event) {
            event.stopPropagation(); // Prevent click event propagation to the document
        });
        contextMenu.appendChild(intentsInput);
        contextMenu.appendChild(document.createElement("br"))

        // Create the entities input field
        var entitiesLabel = document.createElement("label");
        entitiesLabel.textContent = "Entities:";
        contextMenu.appendChild(entitiesLabel);

        var entitiesInput = document.createElement("input");
        entitiesInput.type = "text";
        entitiesInput.value = entities;
        entitiesInput.addEventListener("click", function(event) {
            event.stopPropagation(); // Prevent click event propagation to the document
        });
        contextMenu.appendChild(entitiesInput);

        // Create the "Report Error" button
        var reportButton = document.createElement("button");
        reportButton.textContent = "Report Error";
        reportButton.addEventListener("click", function() {
            // Get the updated values from the input fields
            var updatedIntents = intentsInput.value;
            var updatedEntities = entitiesInput.value;

            // Send a fetch request to the specified URL with the updated values
            var url = "/report?intents=" + encodeURIComponent(updatedIntents) + "&entities=" + encodeURIComponent(updatedEntities) + "&prompt=" + encodeURIComponent(promptText);
            fetch(url)
                .then(function(response) {
                    if(response.status === 200) {
                        let alert = document.getElementById('popup').innerText;
                        document.getElementById('popup').innerText = "Instance successfully added to training data!";
                        showPopup();
                        setTimeout(function() { document.getElementById('popup').innerText = alert; }, 3000)
                    } else {
                        throw new Error
                    }
                })
                .catch(function(error) {
                    let alert = document.getElementById('popup').innerText;
                    document.getElementById('popup').innerText = "Error adding instance to training data!";
                    showPopup();
                    setTimeout(function() { document.getElementById('popup').innerText = alert; }, 1000)
                });

            // Remove the custom right-click menu from the DOM
            contextMenu.remove();
        });
        contextMenu.appendChild(reportButton);

        // Position the custom right-click menu near the cursor
        contextMenu.style.position = "absolute";
        contextMenu.style.left = event.pageX + "px";
        contextMenu.style.top = event.pageY + "px";

	// Position the arrow near the cursor
        arrow.style.position = "absolute";
        arrow.style.left = event.pageX - 5 + "px";
        arrow.style.top = event.pageY + 5 + "px";



        // Append the custom right-click menu to the document body
        document.body.appendChild(contextMenu);

        // Add a listener to remove the custom right-click menu when the user clicks outside of it
        document.addEventListener("click", function() {
            contextMenu.remove();
            arrow.remove();
        });
    }
});


  
</script>
  
</body>

</html>
"""