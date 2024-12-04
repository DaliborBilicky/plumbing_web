const scrollToTopBtn = document.getElementById('scrollToTopBtn')

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

scrollToTopBtn.onclick = function() {
	window.scrollTo({
		top: 0,
		behavior: 'smooth',
	})
}

function deleteReservation(reservationId) {
	if (confirm('Ste si istý, že chcete zmazať rezerváciu?')) {
		fetch(`/delete/${reservationId}/`, {
			method: 'POST',
			headers: {
				'X-CSRFToken': '{{ csrf_token }}',
			},
		}).then((response) => {
			if (response.ok) {
				location.reload()
			} else {
				alert('Nastala chyba pri mazaní.')
			}
		})
	}
}
