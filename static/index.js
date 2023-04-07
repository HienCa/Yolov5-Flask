window.onload = () => {
  const closeImgageLogin = document.getElementById('closeImgageLogin');
  closeImgageLogin.addEventListener('click', function () {
    document.getElementById('BoxImageLogin').style.display = 'none';
  })
  $("#sendbutton").click(() => {
    const loading = document.getElementById('loading');
    loading.style.display = 'block';
    imagebox = $("#imagebox");
    link = $("#link");
    input = $("#imageinput")[0];
    if (input.files && input.files[0]) {
      let formData = new FormData();
      formData.append("video", input.files[0]);
      $.ajax({
        url: "/detect", // fix this to your liking
        type: "POST",
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        error: function (data) {
          console.log("upload error", data);
          console.log(data.getAllResponseHeaders());
        },
        success: function (data) {
          console.log(data);
          if (data.status == 'success') {
            // window.location.href = `/light_system?filename=${data.filename}`;
            // alert("Xác thực hợp lệ!")
            document.getElementById('imageLogin').src = `./static/detectImage/${data.filename}`;
            document.getElementById('BoxImageLogin').style.display = 'block';

            loading.style.display = 'none';
            setTimeout(function () {
              window.location.href = '/light_system';

            }, 1500);


          } else {
            alert("Xác thực thất bại!")
            document.getElementById('imageLogin').src = `./static/nodetectImage/${data.filename}`;

            document.getElementById('BoxImageLogin').style.display = 'block';
            loading.style.display = 'none';

          }

          // $("#link").css("visibility", "visible");
          // $("#download").attr("href", "static/" + data);
          console.log(data);
        },
      });
    }
  });
  $("#opencam").click(() => {
    console.log("evoked openCam");
    $.ajax({
      url: "/opencam",
      type: "GET",
      error: function (data) {
        console.log("upload error", data);
      },
      success: function (data) {
        console.log(data);
        if (data.status == 'success') {
          window.location.href = `/light_system?filename=${data.filename}`;
          alert("Xác thực hợp lệ!")

        } else {
          alert("Xác thực thất bại!")
        }
      }
    });
  })
};

function readUrl(input) {
  imagebox = $("#imagebox");
  console.log(imagebox);
  console.log("evoked readUrl");
  if (input.files && input.files[0]) {
    let reader = new FileReader();
    reader.onload = function (e) {
      console.log(e.target);

      imagebox.attr("src", e.target.result);
      //   imagebox.height(500);
      //   imagebox.width(800);
    };
    reader.readAsDataURL(input.files[0]);
  }
}


function openCam(e) {
  console.log("evoked openCam");
  e.preventDefault();
  console.log("evoked openCam");
  console.log(e);
}