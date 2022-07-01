

$(document).ready(function(){
    setInterval(function(){ 

            const url =$('#list-notif').attr("data-url");
            $.ajax({
                type:'GET',
                url:url,
                success:function(response){
                    $("#list-notif").empty();
                    for(var key in response.notifications){
                        var temp=
                        "<div class='notify_item'><div class='notify_info'><p>"+response.notifications[key].notification+"</p><span class='notify_time'>"+response.notifications[key].date+"</span></div></div>"
                        $("#list-notif").append(temp)
                    }
                },
                error: function(response){
                    alert("no data found")
                }
            })
          
          
    },1000);
})


