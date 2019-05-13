$(function(){
    var member_no = ${"#member_no"}.val();
    alert("ok");
    if (window.sessionStorage) {
        window.sessionStorage.setItem("member_no", member_no);
    }
    if (window.sessionStorage) {
        memberno = window.sessionStorage.getItem("member_no");
    }
    $("#logout").click(function() {
        if (window.sessionStorage) {
            window.sessionStorage.setItem("member_no", 0);
        }
        location.href="http://203.236.209.108:8089/controller/start.jsp";
    });
    $(window).scroll(function() {
        if($(this).scrollTop() > $("#header").height()) {
            $("#navbar").addClass("sticky");
            $("#dropdown-content").css("top", "0");
            $("#btn_top").css("display", "block");
        }
        else {
            $("#navbar").removeClass("sticky");
            $("#dropdown-content").css("top", $("#header").height()-$(this).scrollTop()+60);
            $("#btn_top").css("display", "none");
        }
    });
    $(".btn-menu").click(function(){
        $("#sidebar").css("width", "140px");
        $("#icon-close").css("display", "block");
    });
    $("#icon-close").click(function(){
        $("#sidebar").css("width", "0");
    });
    $("#btn_top").click(function(){
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    });
});