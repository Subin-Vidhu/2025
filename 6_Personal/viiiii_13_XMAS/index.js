// Register GSAP plugins
gsap.registerPlugin(MotionPathPlugin);

// Create snowflakes
function createSnowflakes() {
  const container = document.querySelector(".snowflakesContainer");
  const snowflakeTemplate = document.getElementById("snowflake");
  const numSnowflakes = 100;
  
  for (let i = 0; i < numSnowflakes; i++) {
    const snowflake = snowflakeTemplate.cloneNode(true);
    snowflake.setAttribute("class", "snowflakeInstance");
    snowflake.setAttribute("id", "snowflake" + i);
    container.appendChild(snowflake);
    
    const startX = gsap.utils.random(-100, 1500);
    const startY = gsap.utils.random(-300, -50);
    const duration = gsap.utils.random(15, 30);
    const endX = startX + gsap.utils.random(-200, 200);
    const endY = 900;
    const scale = gsap.utils.random(0.4, 1.3);
    const opacity = gsap.utils.random(0.7, 1);
    const rotationSpeed = gsap.utils.random(-360, 360);
    
    gsap.set(snowflake, {
      x: startX,
      y: startY,
      scale: scale,
      opacity: opacity,
      transformOrigin: "50% 50%"
    });
    
    const tl = gsap.timeline({ repeat: -1, delay: gsap.utils.random(0, 12) });
    tl.to(snowflake, {
      duration: duration,
      x: endX,
      y: endY,
      rotation: rotationSpeed,
      ease: "none"
    })
    .set(snowflake, {
      x: gsap.utils.random(-100, 1500),
      y: gsap.utils.random(-300, -50),
      rotation: 0
    });
  }
}

// Animate reindeer team
function animateReindeerTeam() {
  // Reindeer legs running animation
  gsap.to(".reindeer1 rect, .reindeer2 rect, .reindeer3 rect, .reindeer4 rect, .reindeer5 rect, .reindeer6 rect, .reindeer7 rect, .reindeer8 rect", {
    duration: 0.5,
    y: -8,
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut",
    stagger: {
      each: 0.08,
      from: "random"
    }
  });
  
  // Reindeer antlers swaying
  gsap.to(".reindeer1 path, .reindeer2 path, .reindeer3 path, .reindeer4 path, .reindeer5 path, .reindeer6 path, .reindeer7 path, .reindeer8 path", {
    duration: 1.2,
    rotation: 4,
    transformOrigin: "center center",
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut",
    stagger: 0.15
  });
  
  // Reindeer noses glowing
  gsap.to(".reindeer1 circle[fill='#FF0000'], .reindeer2 circle[fill='#FF0000'], .reindeer3 circle[fill='#FF0000'], .reindeer4 circle[fill='#FF0000'], .reindeer5 circle[fill='#FF0000'], .reindeer6 circle[fill='#FF0000'], .reindeer7 circle[fill='#FF0000'], .reindeer8 circle[fill='#FF0000']", {
    duration: 1.5,
    scale: 1.3,
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut"
  });
  
  // Harness bells jingling
  gsap.to("circle[fill='url(#goldGlow)']", {
    duration: 0.4,
    scale: 1.4,
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut",
    stagger: 0.1
  });
  
  // Main harness line animation
  gsap.to(".mainHarness", {
    duration: 0.6,
    strokeDashoffset: -18,
    repeat: -1,
    ease: "linear"
  });
}

// Animate Santa's sleigh
function animateSleigh() {
  // Sleigh bells jingling
  gsap.to(".sleighGroup circle[fill='url(#goldGlow)']", {
    duration: 0.5,
    rotation: 20,
    transformOrigin: "center center",
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut",
    stagger: 0.2
  });
  
  // Gifts bouncing
  gsap.to(".sleighGroup rect[fill='#FF6B6B'], .sleighGroup rect[fill='#4ECDC4'], .sleighGroup rect[fill='#FFD700']", {
    duration: 2,
    y: -3,
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut",
    stagger: 0.3
  });
  
  // Santa's pointing arm
  gsap.to(".sleighGroup ellipse[transform*='rotate(45']", {
    duration: 2.5,
    rotation: 55,
    transformOrigin: "1200px 370px",
    repeat: -1,
    yoyo: true,
    ease: "sine.inOut"
  });
}

// Main sleigh team animation - flying across the sky
const sleighTl = gsap.timeline({ repeat: -1, repeatDelay: 0.5 });
sleighTl
  .set(".sleighTeam", { x: -300, y: 0, opacity: 0, scale: 0.85 })
  .to(".sleighTeam", {
    duration: 1,
    opacity: 1,
    ease: "power2.out"
  })
  .to(".sleighTeam", {
    duration: 15,
    x: 1700,
    y: -60,
    ease: "power1.inOut"
  })
  .to(".sleighTeam", {
    duration: 0.5,
    opacity: 0,
    ease: "power2.in"
  });

// Initialize all animations
createSnowflakes();
animateReindeerTeam();
animateSleigh();

// Make SVG visible
gsap.set("svg", { visibility: "visible" });
