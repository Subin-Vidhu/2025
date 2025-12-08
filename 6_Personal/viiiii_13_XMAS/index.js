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

// Make the animation loop
mainTl.repeat(-1);
mainTl.repeatDelay(2);

// Adjust time scale for smoother animation
gsap.globalTimeline.timeScale(1.2);
