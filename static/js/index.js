// Get the button
const scrollToTopBtn = document.getElementById('scrollToTopBtn')

// Show the button when scrolling down 200px
window.onscroll = function() {
	if (
		document.body.scrollTop > 200 ||
		document.documentElement.scrollTop > 200
	) {
		scrollToTopBtn.style.display = 'block'
	} else {
		scrollToTopBtn.style.display = 'none'
	}
}

// Scroll to the top when the button is clicked
scrollToTopBtn.onclick = function() {
	window.scrollTo({
		top: 0,
		behavior: 'smooth', // Smooth scroll animation
	})
}
