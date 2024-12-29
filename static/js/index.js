const scrollToTopBtn = document.getElementById('scrollToTopBtn')

window.onscroll = function () {
	if (
		document.body.scrollTop > 200 ||
		document.documentElement.scrollTop > 200
	) {
		scrollToTopBtn.style.display = 'block'
	} else {
		scrollToTopBtn.style.display = 'none'
	}
}

scrollToTopBtn.onclick = function () {
	window.scrollTo({
		top: 0,
		behavior: 'smooth',
	})
}

function deleteReservation(reservationId) {
	if (confirm('Ste si istý, že chcete zmazať rezerváciu?')) {
		fetch(`reservation/delete/${reservationId}/`, {
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

document.addEventListener('DOMContentLoaded', function () {
	const dateField = document.querySelector('[name="date"]')
	const timeField = document.querySelector('[name="time"]')
	const availabilityMessage = document.getElementById('availabilityMessage')

	if (!dateField || !timeField || !availabilityMessage) return

	dateField.addEventListener('change', checkAvailability)
	timeField.addEventListener('change', checkAvailability)

	async function checkAvailability() {
		const selectedDate = dateField.value
		const selectedTime = timeField.value

		if (!selectedDate || !selectedTime) return

		try {
			const response = await fetch('/check_availability/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': document.querySelector(
						'[name="csrfmiddlewaretoken"]'
					).value,
				},
				body: JSON.stringify({
					date: selectedDate,
					time: selectedTime,
				}),
			})

			const data = await response.json()

			if (data.available) {
				availabilityMessage.textContent = 'Tento termín je dostupný!'
				availabilityMessage.style.color = 'green'
			} else {
				availabilityMessage.textContent =
					'Ľutujeme, tento termín je už rezervovaný.'
				availabilityMessage.style.color = 'red'
			}
		} catch (error) {
			console.error('Error checking availability:', error)
		}
	}
})

document.addEventListener('DOMContentLoaded', () => {
	const showPasswordCheckbox = document.getElementById('showPasswordCheckbox')
	if (showPasswordCheckbox) {
		showPasswordCheckbox.addEventListener('change', function () {
			const passwordField = document.querySelector(
				'input[name="password"]'
			)
			if (passwordField) {
				passwordField.type = this.checked ? 'text' : 'password'
			}
		})
	}
})

document.addEventListener('DOMContentLoaded', () => {
	const showPasswordCheckbox = document.getElementById(
		'showPasswordCheckbox2'
	)
	if (showPasswordCheckbox) {
		showPasswordCheckbox.addEventListener('change', function () {
			const passwordField = document.querySelector(
				'input[name="password_confirmation"]'
			)
			if (passwordField) {
				passwordField.type = this.checked ? 'text' : 'password'
			}
		})
	}
})
