$('audio').on('play', function() {
    var triggerd = false;
    return function(e) {
        if (triggerd) return;
        triggerd = true;
        console.log(e.target.currentSrc);

        var url = new URL('http://localhost:35528/notify');
        url.search = new URLSearchParams({
            'timestamp': Math.round(new Date().getTime()/1000)
        });
        fetch(url).then(function(response){
            response.json().then(function(j){console.log(j);});
        }).catch(function(error) {
            console.log(error);
        });
    };
}());