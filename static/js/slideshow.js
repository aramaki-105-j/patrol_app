let currentIndex = 0;
const images = document.querySelectorAll('.slide');
images[currentIndex].style.opacity = 1;

setInterval(() => {
  images[currentIndex].style.opacity = 0;
  currentIndex = (currentIndex + 1) % images.length;
  images[currentIndex].style.opacity = 1;
}, 4000); // 4秒ごとに画像を切り替え      