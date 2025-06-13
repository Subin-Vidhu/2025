// wrote the code in js browser console

// Simple case
const nemo = ["Nemo"]

function findNemo(array){
    for (let i=0; i<array.length;i++){
        if(array[i]=="Nemo"){
            console.log("Found Nemo");
        }
    }
}


findNemo(nemo)

// Larger and Larger arrays
const everyone = [
  "Nemo",
  "Marlin",
  "Dory",
  "Bruce",
  "Crush",
  "Squirt",
  "Gill",
  "Bloat",
  "Peach",
  "Gurgle"
];
const large = new Array(1000).fill("Nemo");
function findNemo(array){
    let t0 = performance.now()
    for (let i=0; i<array.length;i++){
        if(array[i]=="Nemo"){
            console.log("Found Nemo");
        }
    }
    t1 = performance.now()
    console.log("Call to find Nemo took " + (t1-t0)+ "ms");
}

findNemo(nemo)
findNemo(everyone)
findNemo(large)

