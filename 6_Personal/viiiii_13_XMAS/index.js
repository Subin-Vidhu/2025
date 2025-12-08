// Register GSAP plugins
gsap.registerPlugin(MotionPathPlugin);

// Try to register premium plugins if available
if (typeof MorphSVGPlugin !== "undefined") {
  gsap.registerPlugin(MorphSVGPlugin);
  MorphSVGPlugin.convertToPath("polygon");
}
if (typeof DrawSVGPlugin !== "undefined") {
  gsap.registerPlugin(DrawSVGPlugin);
}
if (typeof Physics2DPlugin !== "undefined") {
  gsap.registerPlugin(Physics2DPlugin);
}

var xmlns = "http://www.w3.org/2000/svg",
  xlinkns = "http://www.w3.org/1999/xlink",
  select = function (s) {
    return document.querySelector(s);
  },
  selectAll = function (s) {
    return document.querySelectorAll(s);
  },
  pContainer = select(".pContainer"),
  mainSVG = select(".mainSVG"),
  star = select("#star"),
  sparkle = select(".sparkle"),
  tree = select("#tree"),
  showParticle = true,
  particleColorArray = [
    "#FFD700", // Gold
    "#FF6B6B", // Red
    "#4ECDC4", // Teal
    "#FFE66D", // Yellow
    "#FF8B94", // Pink
    "#95E1D3", // Mint
    "#F38181", // Coral
    "#AA96DA", // Purple
    "#FCBAD3", // Light Pink
    "#FFD93D", // Bright Yellow
    "#6BCB77", // Green
    "#FF6B9D"  // Hot Pink
  ],
  particleTypeArray = ["#star", "#circ", "#cross", "#heart"],
  particlePool = [],
  particleCount = 0,
  numParticles = 300; // Increased for more particles

gsap.set("svg", {
  visibility: "visible"
});

gsap.set(sparkle, {
  transformOrigin: "50% 50%",
  y: -100,
  scale: 1.2,
  filter: "url(#glow)"
});

// Add pulsing animation to sparkle
gsap.to(sparkle, {
  scale: 1.5,
  duration: 0.8,
  repeat: -1,
  yoyo: true,
  ease: "sine.inOut"
});

let getSVGPoints = (path) => {
  let arr = [];
  var rawPath = MotionPathPlugin.getRawPath(path)[0];
  rawPath.forEach((el, value) => {
    let obj = {};
    obj.x = rawPath[value * 2];
    obj.y = rawPath[value * 2 + 1];
    if (value % 2) {
      arr.push(obj);
    }
    //console.log(value)
  });

  return arr;
};
let treePath = getSVGPoints(".treePath");
var treeBottomPath = getSVGPoints(".treeBottomPath");

// Initialize sparkle position at start of tree path
if (treePath && treePath.length > 0) {
  gsap.set(".pContainer, .sparkle", {
    x: treePath[0].x,
    y: treePath[0].y
  });
}

//console.log(starPath.length)
var mainTl = gsap.timeline({ delay: 0, repeat: 0 }),
  starTl;

//tl.seek(100).timeScale(1.82)

function flicker(p) {
  gsap.killTweensOf(p, { opacity: true });
  gsap.fromTo(
    p,
    {
      opacity: 1
    },
    {
      duration: gsap.utils.random(0.05, 0.15),
      opacity: gsap.utils.random(0.3, 1),
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut"
    }
  );
}

function createParticles() {
  //var step = numParticles/starPath.length;
  //console.log(starPath.length)
  var i = numParticles,
    p,
    particleTl,
    step = numParticles / treePath.length,
    pos;
  while (--i > -1) {
    p = select(particleTypeArray[i % particleTypeArray.length]).cloneNode(true);
    mainSVG.appendChild(p);
    p.setAttribute("fill", particleColorArray[i % particleColorArray.length]);
    p.setAttribute("class", "particle");
    particlePool.push(p);
    //hide them initially
    gsap.set(p, {
      x: -100,
      y: -100,
      transformOrigin: "50% 50%"
    });
  }
}

var getScale = gsap.utils.random(0.5, 3, 0.001, true);

function playParticle(p) {
  if (!showParticle) {
    return;
  }
  var p = particlePool[particleCount];
  var startX = gsap.getProperty(".pContainer", "x") || 0;
  var startY = gsap.getProperty(".pContainer", "y") || 0;
  
  gsap.set(p, {
    x: startX,
    y: startY,
    scale: getScale(),
    opacity: 1
  });
  
  var tl = gsap.timeline();
  var angle = gsap.utils.random(-180, 180);
  var velocity = gsap.utils.random(50, 150);
  var distance = gsap.utils.random(80, 200);
  var endX = startX + Math.cos(angle * Math.PI / 180) * distance;
  var endY = startY + Math.sin(angle * Math.PI / 180) * distance + gsap.utils.random(50, 150);
  
  // Use physics2D if available, otherwise use regular animation
  var animProps = {
    duration: gsap.utils.random(1.5, 4),
    x: endX,
    y: endY,
    scale: 0,
    rotation: gsap.utils.random(-360, 360),
    ease: "power2.out",
    onStart: flicker,
    onStartParams: [p]
  };
  
  if (typeof Physics2DPlugin !== "undefined") {
    animProps.physics2D = {
      velocity: gsap.utils.random(-23, 23),
      angle: angle,
      gravity: gsap.utils.random(50, 150)
    };
    delete animProps.x;
    delete animProps.y;
  }
  
  tl.to(p, animProps);

  particleCount++;
  particleCount = particleCount >= numParticles ? 0 : particleCount;
}

function drawStar() {
  starTl = gsap.timeline({ 
    onUpdate: playParticle,
    repeat: -1,
    repeatDelay: 0.5
  });
  starTl
    .to(".pContainer, .sparkle", {
      duration: 6,
      motionPath: {
        path: ".treePath",
        autoRotate: false
      },
      ease: "linear"
    })
    .to(".pContainer, .sparkle", {
      duration: 1,
      onStart: function () {
        showParticle = false;
      },
      x: treeBottomPath[0].x,
      y: treeBottomPath[0].y
    })
    .to(
      ".pContainer, .sparkle",
      {
        duration: 2,
        onStart: function () {
          showParticle = true;
        },
        motionPath: {
          path: ".treeBottomPath",
          autoRotate: false
        },
        ease: "linear"
      },
      "-=0"
    )
    .from(
      ".treeBottomMask",
      {
        duration: 2,
        drawSVG: typeof DrawSVGPlugin !== "undefined" ? "0% 0%" : undefined,
        strokeDasharray: typeof DrawSVGPlugin === "undefined" ? "1000" : undefined,
        strokeDashoffset: typeof DrawSVGPlugin === "undefined" ? "1000" : undefined,
        stroke: "#FFF",
        ease: "linear"
      },
      "-=2"
    )
    .set(".pContainer, .sparkle", {
      x: treePath && treePath.length > 0 ? treePath[0].x : 0,
      y: treePath && treePath.length > 0 ? treePath[0].y : 0
    });

  //gsap.staggerTo(particlePool, 2, {})
}

createParticles();
drawStar();
//ScrubGSAPTimeline(mainTl)

mainTl
  .from([".treePathMask", ".treePotMask"], {
    duration: 6,
    drawSVG: typeof DrawSVGPlugin !== "undefined" ? "0% 0%" : undefined,
    strokeDasharray: typeof DrawSVGPlugin === "undefined" ? "1000" : undefined,
    strokeDashoffset: typeof DrawSVGPlugin === "undefined" ? "1000" : undefined,
    stroke: "#FFF",
    stagger: {
      each: 6
    },
    duration: gsap.utils.wrap([6, 1, 2]),
    ease: "linear"
  })
  .from(
    ".treeStar",
    {
      duration: 3,
      //skewY:270,
      scaleY: 0,
      scaleX: 0.15,
      transformOrigin: "50% 50%",
      ease: "elastic(1,0.5)"
    },
    "-=4"
  )

  .to(
    ".sparkle",
    {
      duration: 3,
      opacity: 0,
      ease: typeof RoughEase !== "undefined" 
        ? "rough({strength: 2, points: 100, template: linear, taper: both, randomize: true, clamp: false})"
        : "power2.in"
    },
    "-=0"
  )
  .to(
    ".treeStarOutline",
    {
      duration: 1,
      opacity: 1,
      ease: typeof RoughEase !== "undefined"
        ? "rough({strength: 2, points: 16, template: linear, taper: none, randomize: true, clamp: false})"
        : "power2.out"
    },
    "+=1"
  );
/* .to('.whole', {
  opacity: 0
}, '+=2') */

mainTl.add(starTl, 0);

// Animate Santa and Sleigh - Moving all around the page
var santaTl = gsap.timeline({ repeat: -1, repeatDelay: 2 });
santaTl
  .set(".santaGroup", { x: -150, y: 50, opacity: 0, scale: 0.8, rotation: -15 })
  .to(".santaGroup", {
    duration: 0.5,
    opacity: 1,
    ease: "power2.out"
  })
  // Complex path moving around the entire page
  .to(".santaGroup", {
    duration: 3,
    x: 200,
    y: 80,
    rotation: 5,
    ease: "power1.inOut"
  })
  .to(".santaGroup", {
    duration: 3,
    x: 500,
    y: 40,
    rotation: -10,
    ease: "power1.inOut"
  })
  .to(".santaGroup", {
    duration: 3,
    x: 750,
    y: 100,
    rotation: 15,
    ease: "power1.inOut"
  })
  .to(".santaGroup", {
    duration: 3,
    x: 950,
    y: 60,
    rotation: 10,
    ease: "power1.inOut"
  })
  .to(".santaGroup", {
    duration: 0.5,
    opacity: 0,
    ease: "power2.in"
  });

// Animate Reindeers - Moving all around with different paths
var reindeerTl1 = gsap.timeline({ repeat: -1, repeatDelay: 3 });
reindeerTl1
  .set(".reindeerGroup1", { x: -100, y: 100, opacity: 0, scale: 0.7, rotation: -12 })
  .to(".reindeerGroup1", {
    duration: 0.5,
    opacity: 1,
    ease: "power2.out"
  })
  .to(".reindeerGroup1", {
    duration: 2.5,
    x: 150,
    y: 120,
    rotation: 8,
    ease: "power1.inOut"
  })
  .to(".reindeerGroup1", {
    duration: 2.5,
    x: 400,
    y: 80,
    rotation: -5,
    ease: "power1.inOut"
  })
  .to(".reindeerGroup1", {
    duration: 2.5,
    x: 650,
    y: 110,
    rotation: 12,
    ease: "power1.inOut"
  })
  .to(".reindeerGroup1", {
    duration: 2.5,
    x: 900,
    y: 90,
    rotation: 8,
    ease: "power1.inOut"
  })
  .to(".reindeerGroup1", {
    duration: 0.5,
    opacity: 0,
    ease: "power2.in"
  });

var reindeerTl2 = gsap.timeline({ repeat: -1, repeatDelay: 4 });
reindeerTl2
  .set(".reindeerGroup2", { x: 950, y: 120, opacity: 0, scale: 0.7, rotation: 12 })
  .to(".reindeerGroup2", {
    duration: 0.5,
    opacity: 1,
    ease: "power2.out"
  })
  .to(".reindeerGroup2", {
    duration: 2.5,
    x: 700,
    y: 100,
    rotation: -8,
    ease: "power1.inOut"
  })
  .to(".reindeerGroup2", {
    duration: 2.5,
    x: 450,
    y: 130,
    rotation: 5,
    ease: "power1.inOut"
  })
  .to(".reindeerGroup2", {
    duration: 2.5,
    x: 200,
    y: 90,
    rotation: -12,
    ease: "power1.inOut"
  })
  .to(".reindeerGroup2", {
    duration: 2.5,
    x: -50,
    y: 110,
    rotation: -8,
    ease: "power1.inOut"
  })
  .to(".reindeerGroup2", {
    duration: 0.5,
    opacity: 0,
    ease: "power2.in"
  });

var reindeerTl3 = gsap.timeline({ repeat: -1, repeatDelay: 2.5 });
reindeerTl3
  .set(".reindeerGroup3", { x: 400, y: -50, opacity: 0, scale: 0.6, rotation: 0 })
  .to(".reindeerGroup3", {
    duration: 0.5,
    opacity: 1,
    ease: "power2.out"
  })
  .to(".reindeerGroup3", {
    duration: 2,
    x: 300,
    y: 70,
    rotation: -10,
    ease: "power1.inOut"
  })
  .to(".reindeerGroup3", {
    duration: 2,
    x: 600,
    y: 50,
    rotation: 10,
    ease: "power1.inOut"
  })
  .to(".reindeerGroup3", {
    duration: 2,
    x: 500,
    y: 130,
    rotation: -5,
    ease: "power1.inOut"
  })
  .to(".reindeerGroup3", {
    duration: 2,
    x: 200,
    y: 100,
    rotation: 8,
    ease: "power1.inOut"
  })
  .to(".reindeerGroup3", {
    duration: 2,
    x: 800,
    y: 80,
    rotation: -8,
    ease: "power1.inOut"
  })
  .to(".reindeerGroup3", {
    duration: 0.5,
    opacity: 0,
    ease: "power2.in"
  });

// Animate Presents
var presentsTl = gsap.timeline({ delay: 8, repeat: -1, repeatDelay: 5 });
presentsTl
  .from(".presentsGroup", {
    duration: 1,
    opacity: 0,
    y: 20,
    scale: 0.5,
    ease: "back.out(1.7)",
    stagger: 0.2
  })
  .to(".present1, .present2, .present3", {
    duration: 0.3,
    scale: 1.1,
    yoyo: true,
    repeat: 1,
    ease: "power2.inOut",
    stagger: 0.1
  })
  .to(".present1Bow, .present2Bow, .present3Bow", {
    duration: 0.5,
    rotation: 360,
    transformOrigin: "50% 50%",
    repeat: 2,
    ease: "power2.inOut",
    stagger: 0.1
  }, "-=0.5")
  .to(".presentsGroup", {
    duration: 0.5,
    opacity: 0,
    delay: 2
  });

// Continuous sparkle on presents
gsap.to(".present1Bow, .present2Bow, .present3Bow", {
  duration: 2,
  scale: 1.2,
  opacity: 0.8,
  repeat: -1,
  yoyo: true,
  ease: "sine.inOut",
  stagger: 0.3
});

// Create and animate snowflakes - Falling all around the page
function createSnowflakes() {
  var snowflakesContainer = select(".snowflakesContainer");
  var numSnowflakes = 50; // More snowflakes
  
  for (var i = 0; i < numSnowflakes; i++) {
    var snowflake = select("#snowflake").cloneNode(true);
    snowflake.setAttribute("class", "snowflakeInstance");
    snowflake.setAttribute("id", "snowflake" + i);
    snowflakesContainer.appendChild(snowflake);
    
    // Start from random positions across the entire width
    var startX = gsap.utils.random(-50, 850);
    var startY = gsap.utils.random(-200, -50);
    var duration = gsap.utils.random(10, 20);
    // Snowflakes drift horizontally as they fall
    var endX = startX + gsap.utils.random(-100, 100);
    var endY = 650; // Fall past the bottom
    var scale = gsap.utils.random(0.2, 1);
    var opacity = gsap.utils.random(0.5, 1);
    var rotationSpeed = gsap.utils.random(-360, 360);
    
    gsap.set(snowflake, {
      x: startX,
      y: startY,
      scale: scale,
      opacity: opacity,
      transformOrigin: "50% 50%"
    });
    
    // Create continuous falling animation
    var tl = gsap.timeline({ repeat: -1, delay: gsap.utils.random(0, 8) });
    tl.to(snowflake, {
      duration: duration,
      x: endX,
      y: endY,
      rotation: rotationSpeed,
      ease: "none" // Linear fall
    })
    .set(snowflake, {
      x: gsap.utils.random(-50, 850), // Reset to random X position
      y: gsap.utils.random(-200, -50), // Reset above screen
      rotation: 0
    });
  }
}

// Animate reindeer antlers and legs
function animateReindeer() {
  // Reindeer 1 antlers
  gsap.to(".antlers1", {
    duration: 0.6,
    rotation: 6,
    transformOrigin: "50% 50%",
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut"
  });
  
  // Reindeer 2 antlers
  gsap.to(".antlers2", {
    duration: 0.6,
    rotation: -6,
    transformOrigin: "50% 50%",
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut"
  });
  
  // Reindeer 3 antlers
  gsap.to(".antlers3", {
    duration: 0.6,
    rotation: 6,
    transformOrigin: "50% 50%",
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut"
  });
  
  // Reindeer ears twitching
  gsap.to(".reindeerEar1, .reindeerEar3, .reindeerEar5", {
    duration: 0.3,
    rotation: -10,
    transformOrigin: "50% 50%",
    repeat: -1,
    repeatDelay: 2,
    yoyo: true,
    ease: "power2.inOut"
  });
  
  gsap.to(".reindeerEar2, .reindeerEar4, .reindeerEar6", {
    duration: 0.3,
    rotation: 10,
    transformOrigin: "50% 50%",
    repeat: -1,
    repeatDelay: 2,
    yoyo: true,
    ease: "power2.inOut"
  });
  
  // Reindeer noses glow
  gsap.to(".reindeerNose1, .reindeerNose2", {
    duration: 1.2,
    scale: 1.3,
    opacity: 0.9,
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut"
  });
  
  // Rudolph's nose - extra glow!
  gsap.to(".reindeerNose3", {
    duration: 0.7,
    scale: 1.4,
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut"
  });
  
  gsap.to(".reindeerNose3Glow", {
    duration: 0.7,
    scale: 1.6,
    opacity: 0.7,
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut"
  });
  
  // Reindeer legs moving (running motion)
  gsap.to(".leg1, .leg4, .leg7", {
    duration: 0.4,
    y: -2,
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut",
    stagger: 0.1
  });
  
  gsap.to(".leg2, .leg5, .leg8", {
    duration: 0.4,
    y: 2,
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut",
    stagger: 0.1
  });
}

// Animate Santa's hat and bag
function animateSanta() {
  gsap.to(".santaHat", {
    duration: 0.4,
    y: -2,
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut"
  });
  
  gsap.to(".hatPom", {
    duration: 0.3,
    scale: 1.1,
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut"
  });
  
  gsap.to(".santaBag", {
    duration: 0.6,
    rotation: 8,
    transformOrigin: "50% 50%",
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut"
  });
  
  // Santa waving (subtle)
  gsap.to(".santaBody", {
    duration: 2.5,
    rotation: 3,
    transformOrigin: "50% 50%",
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut"
  });
  
  // Santa's eyes blinking
  gsap.to(".santaEye1, .santaEye2", {
    duration: 0.1,
    scaleY: 0.1,
    repeat: -1,
    repeatDelay: 3,
    yoyo: true,
    ease: "power2.inOut"
  });
  
  // Sleigh runners moving
  gsap.to(".sleighRunner1, .sleighRunner2", {
    duration: 0.5,
    rotation: 5,
    transformOrigin: "50% 50%",
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut"
  });
}

// Initialize all animations
createSnowflakes();
animateReindeer();
animateSanta();

// Make the animation loop
mainTl.repeat(-1);
mainTl.repeatDelay(2);

// Adjust time scale for smoother animation
gsap.globalTimeline.timeScale(1.2);
