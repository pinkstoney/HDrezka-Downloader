(function() {
    function clearTrash(data){
        function product(iterables, repeat) {
            var argv = Array.prototype.slice.call(arguments), argc = argv.length;
            if (argc === 2 && !isNaN(argv[argc - 1])) {
                var copies = [];
                for (var i = 0; i < argv[argc - 1]; i++) {
                    copies.push(argv[0].slice()); 
                }
                argv = copies;
            }
            return argv.reduce(function tl(accumulator, value) {
                var tmp = [];
                accumulator.forEach(function(a0) {
                    value.forEach(function(a1) {
                        tmp.push(a0.concat(a1));
                    });
                });
                return tmp;
            }, [[]]);
        }
        function unite(arr){
            var final = [];
            arr.forEach(function(e){
                final.push(e.join(""))
            })
            return final;
        }
        var trashList = ["@","#","!","^","$"];
        var two = unite(product(trashList, 2));
        var tree = unite(product(trashList, 3));
        var trashCodesSet = two.concat(tree);

        var arr = data.replace("#h", "").split("//_//");
        var trashString = arr.join('');

        trashCodesSet.forEach(function(i){
            var temp = btoa(i)
            trashString = trashString.replaceAll(temp, '')
        })

        var final_string = atob(trashString);
        return final_string;
    }

    console.log(clearTrash(CDNPlayerInfo.streams));
})();

