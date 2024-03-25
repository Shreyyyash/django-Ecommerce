
$('.plus-cart').click(function(){
    var id=$(this).attr('pid').toString();
    var eml=(this.parentNode.children[2])
    console.log("pid",id)
    $.ajax({
            type: "GET",
            url: "/plus_cart",
            data: {
                prod_id:id,               
            },
            success: function(data) {
                // Handle success response
                console.log("data=",data);
                eml.innerText=data.quantity
                document.getElementById("amount").innerText=data.amount
                document.getElementById("totalamount").innerText=data.totalamount
            },
            
    })
})
$('.minus-cart').click(function(){
    var id=$(this).attr('pid').toString();
    var eml=(this.parentNode.children[2])
    console.log("pid",id)
    $.ajax({
            type: "GET",
            url: "/minus_cart",
            data: {
                prod_id:id,               
            },
            success: function(data) {
                // Handle success response
                console.log("data=",data);
                eml.innerText=data.quantity
                document.getElementById("amount").innerText=data.amount
                document.getElementById("totalamount").innerText=data.totalamount
            },
            
    })
})

$('.plus-wishlist').click(function(){
    var id = $(this).attr('pid').toString();
    $.ajax({
        type:"GET",
        url:'/pluswishlist',
        data:{
            prod_id:id
        },
        success:function(data){
            alert(data.message)
            window.location.href=`http://localhost:8000/category/products/${id}`
        }

    })
})
$('.minus-wishlist').click(function(){
    var id=$(this).attr('pid').toString();
    $.ajax({
        type:"GET",
        url:'/minuswishlist',
        data:{
            prod_id:id
        },
        success:function(data){
            alert(data.message)
            window.location.href=`http://localhost:8000/category/products/${id}`
        }

    })
})
    