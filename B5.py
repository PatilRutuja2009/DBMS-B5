> db.orders11.insert({"Cust_id":"a11","Order_date":newDate("oct 04,2012"),"Status":"A","Price":25,"Gender":"M","Rating":2})
Mon Oct  7 08:51:20.458 ReferenceError: newDate is not defined
> db.orders11.insert({"Cust_id":"a11","Order_date":new Date("oct 04,2012"),"Status":"A","Price":25,"Gender":"M","Rating":2})
> db.orders11.insert({"Cust_id":"a12","Order_date":new Date("may 06,2015"),"Status":"P","Price":35,"Gender":"F","Rating":3})
> db.orders11.insert({"Cust_id":"a105","Order_date":new Date("jun 14,2017"),"Status":"A","Price":55,"Gender":"M","Rating":2.5})
> db.orders11.insert({"Cust_id":"a80","Order_date":new Date("dec 31,2013"),"Status":"P","Price":350,"Gender":"F","Rating":5})
> db.orders11.insert({"Cust_id":"a40","Order_date":new Date("mar 22,2016"),"Status":"A","Price":650,"Gender":"M","Rating":4.5})
> db.orders11.find().pretty()
{
    "_id" : ObjectId("5d9aaf708f0a6f7885d6cc1b"),
    "Cust_id" : "a11",
    "Order_date" : ISODate("2012-10-03T18:30:00Z"),
    "Status" : "A",
    "Price" : 25,
    "Gender" : "M",
    "Rating" : 2
}
{
    "_id" : ObjectId("5d9aafb18f0a6f7885d6cc1c"),
    "Cust_id" : "a12",
    "Order_date" : ISODate("2015-05-05T18:30:00Z"),
    "Status" : "P",
    "Price" : 35,
    "Gender" : "F",
    "Rating" : 3
}
{
    "_id" : ObjectId("5d9aafe78f0a6f7885d6cc1d"),
    "Cust_id" : "a105",
    "Order_date" : ISODate("2017-06-13T18:30:00Z"),
    "Status" : "A",
    "Price" : 55,
    "Gender" : "M",
    "Rating" : 2.5
}
{
    "_id" : ObjectId("5d9ab01f8f0a6f7885d6cc1e"),
    "Cust_id" : "a80",
    "Order_date" : ISODate("2013-12-30T18:30:00Z"),
    "Status" : "P",
    "Price" : 350,
    "Gender" : "F",
    "Rating" : 5
}
{
    "_id" : ObjectId("5d9ab0dc8f0a6f7885d6cc1f"),
    "Cust_id" : "a40",
    "Order_date" : ISODate("2016-03-21T18:30:00Z"),
    "Status" : "A",
    "Price" : 650,
    "Gender" : "M",
    "Rating" : 4.5
}
> db.orders11.mapReduce(function(){emit(this.Cust_id,this.Price);},function(key,value){return Array.sum(value)},{out:"Result"})
{
    "result" : "Result",
    "timeMillis" : 128,
    "counts" : {
        "input" : 5,
        "emit" : 5,
        "reduce" : 0,
        "output" : 5
    },
    "ok" : 1,
}
> db.Result.find().pretty()
{ "_id" : "a105", "value" : 55 }
{ "_id" : "a11", "value" : 25 }
{ "_id" : "a12", "value" : 35 }
{ "_id" : "a40", "value" : 650 }
{ "_id" : "a80", "value" : 350 }
> db.orders11.insert({"Cust_id":"a40","Order_date":new Date("mar 22,2016"),"Status":"A","Price":50,"Gender":"M","Rating":4.5})
> db.orders11.insert({"Cust_id":"a40","Order_date":new Date("mar 22,2016"),"Status":"A","Price":500,"Gender":"M","Rating":4.5})
> db.orders11.mapReduce(function(){emit(this.Cust_id,this.Price);},function(key,value){return Array.sum(value)},{out:"Result"})
{
    "result" : "Result",
    "timeMillis" : 4,
    "counts" : {
        "input" : 7,
        "emit" : 7,
        "reduce" : 1,
        "output" : 5
    },
    "ok" : 1,
}
> db.Result.find().pretty()
{ "_id" : "a105", "value" : 55 }
{ "_id" : "a11", "value" : 25 }
{ "_id" : "a12", "value" : 35 }
{ "_id" : "a40", "value" : 1200 }
{ "_id" : "a80", "value" : 350 }
> var map=function(){var gen;if(this.Gender=='M')gen="Male";else gen="Female";emit(gen,Cust_id)};
> var map=function(){var gen;if(this.Gender=='M')gen="Male";else gen="Female";emit(gen,this.Cust_id)};
> var reduce=function(key,value){var sum=0; value.forEach(function(doc){sum=sum+1});return{total:sum};};
> db.orders11.mapReduce(map,reduce,{out:"Result1"})
{
    "result" : "Result1",
    "timeMillis" : 32,
    "counts" : {
        "input" : 7,
        "emit" : 7,
        "reduce" : 2,
        "output" : 2
    },
    "ok" : 1,
}
> db.Result1.find()
{ "_id" : "Female", "value" : { "total" : 2 } }
{ "_id" : "Male", "value" : { "total" : 5 } }
> var map=function(){var Ratings;if(this.Rating>=1 && this.Rating<2)Ratings=1; else if(this.Rating>=2 && this.Rating<3)Ratings=2;else if(this.Rating>=3 && this.Rating<4)Ratings=3; else if(this.Rating>=4 && this.Rating<5 )Ratings=4; else Ratings=5;emit(Ratings,this.Cust_id);}
> var reduce=function(key,value){var sum=0;value.forEach(function(doc){sum=sum+1});return{total:sum}};
> db.orders11.mapReduce(map,reduce,{out:"Result2"})
{
    "result" : "Result2",
    "timeMillis" : 12,
    "counts" : {
        "input" : 7,
        "emit" : 7,
        "reduce" : 2,
        "output" : 4
    },
    "ok" : 1,
}
> db.Result2.find()
{ "_id" : 2, "value" : { "total" : 2 } }
{ "_id" : 3, "value" : "a12" }
{ "_id" : 4, "value" : { "total" : 3 } }
{ "_id" : 5, "value" : "a80" }
> var map=function(){var Ratings;if(this.Rating>=1 && this.Rating<2)Ratings=1; else if(this.Rating>=2 && this.Rating<3)Ratings=2;else if(this.Rating>=3 && this.Rating<4)Ratings=3; else if(this.Rating>=4 && this.Rating<5 )Ratings=4; else Ratings=5;emit(Ratings,this.Cust_id);}
> var reduce=function(key,value){var sum=0,avg=0,ratingsum=0;value.forEach(function(doc){sum=sum+1;ratingsum=ratingsum+key});avg=ratingsum/sum;return{total:avg}};
> db.orders11.mapReduce(map,reduce,{out:"Result2"})
{
    "result" : "Result2",
    "timeMillis" : 20,
    "counts" : {
        "input" : 7,
        "emit" : 7,
        "reduce" : 2,
        "output" : 4
    },
    "ok" : 1,
}
> db.Result2.find()
{ "_id" : 2, "value" : { "total" : 2 } }
{ "_id" : 3, "value" : "a12" }
{ "_id" : 4, "value" : { "total" : 4 } }
{ "_id" : 5, "value" : "a80" }
> var map=function(){var Ratings;if(this.Rating>=1 && this.Rating<2)Ratings=1; else if(this.Rating>=2 && this.Rating<3)Ratings=2;else if(this.Rating>=3 && this.Rating<4)Ratings=3; else if(this.Rating>=4 && this.Rating<5 )Ratings=4; else Ratings=5;emit(this.Cust_id,Ratings);}
> var reduce=function(key,value){var sum=0,avg=0,ratingsum=0;value.forEach(function(doc){sum=sum+1;ratingsum=ratingsum+value});avg=ratingsum/sum;return{total:avg}};
> db.orders11.mapReduce(map,reduce,{out:"Result2"})
{
    "result" : "Result2",
    "timeMillis" : 7,
    "counts" : {
        "input" : 7,
        "emit" : 7,
        "reduce" : 1,
        "output" : 5
    },
    "ok" : 1,
}
> db.Result2.find()
{ "_id" : "a105", "value" : 2 }
{ "_id" : "a11", "value" : 2 }
{ "_id" : "a12", "value" : 3 }
{ "_id" : "a40", "value" : { "total" : NaN } }
{ "_id" : "a80", "value" : 5 }
