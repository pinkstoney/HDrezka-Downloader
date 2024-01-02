function productNew(iterables, repeat) {
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
  
  const unite = arr => arr.map(e => e.join(""));
  
  const clearTrash = data => {
    const trashList = ["@", "#", "!", "^", "$"];
    const trashCodesSet = unite(productNew(trashList, 2)).concat(unite(productNew(trashList, 3)));
    let trashString = data.replace("#h", "").split("//_//").join('');
    trashCodesSet.forEach(i => trashString = trashString.replaceAll(btoa(i), ''));
    return atob(trashString);
  };
  
  const clickElement = selector => {
    const element = $(selector)[0];
    if (element) {
        if (document.createEvent) {
            const event = new MouseEvent("click", {bubbles: true, cancelable: true, view: window});
            element.dispatchEvent(event);
        } else if (element.fireEvent) {
            element.fireEvent("onclick");
        }
    } else {
        console.log('Element does not exist');
    }
};

const selector = '.b-translator__item[data-translator_id="238"]';
clickElement(selector);

setTimeout(() => console.log(clearTrash(CDNPlayerInfo.streams)), 1000);