document.addEventListener("DOMContentLoaded", () => {
    const btnUp = document.getElementById("btn-up");
    const btnDown = document.getElementById("btn-down");
    const btnLeft = document.getElementById("btn-left");
    const btnRight = document.getElementById("btn-right");
    const btnPause = document.getElementById("btn-pause");
    const btnEnd = document.getElementById("btn-end");

    console.log("javaScript engaged")
  
    btnUp.addEventListener("click", () => {
      changeDirection("up");
    });
  
    btnDown.addEventListener("click", () => {
      changeDirection("down");
    });
  
    btnLeft.addEventListener("click", () => {
      changeDirection("left");
    });
  
    btnRight.addEventListener("click", () => {
      changeDirection("right");
    });
  
    btnPause.addEventListener("click", () => {
      // Handle pause button click
    });
  
    btnEnd.addEventListener("click", () => {
      // Handle end button click
    });
  
    function changeDirection(newDirection) {
      // Send an AJAX request to update the game direction
      const url = "/game/change_direction/";
      const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
      const data = JSON.stringify({ direction: newDirection });
  
      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: data,
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Failed to update direction");
          }
        })
        .catch((error) => {
          console.error(error);
        });
    }
  });
  