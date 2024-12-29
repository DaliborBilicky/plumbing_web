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

document.addEventListener('DOMContentLoaded', function () {
	const passwordField = document.querySelector('[name="password"]')
	const confirmPasswordField = document.querySelector(
		'[name="password_confirmation"]'
	)
	const passwordMatchMessage = document.getElementById('passwordMatchMessage')

	if (!passwordField || !confirmPasswordField || !passwordMatchMessage) return

	confirmPasswordField.addEventListener('input', checkPasswordMatch)

	async function checkPasswordMatch() {
		const password = passwordField.value
		const confirmPassword = confirmPasswordField.value

		if (password !== '' && confirmPassword !== '') {
			try {
				const response = await fetch('/check_password_match/', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'X-CSRFToken': document.querySelector(
							'[name="csrfmiddlewaretoken"]'
						).value,
					},
					body: JSON.stringify({
						password: password,
						confirm_password: confirmPassword,
					}),
				})
				const data = await response.json()
				if (data.match) {
					passwordMatchMessage.textContent = 'Heslá sa zhodujú'
					passwordMatchMessage.style.color = 'green'
				} else {
					passwordMatchMessage.textContent = 'Heslá sa nezhodujú'
					passwordMatchMessage.style.color = 'red'
				}
			} catch (error) {
				console.error('Error during password check:', error)
			}
		} else {
			passwordMatchMessage.textContent = ''
		}
	}
})

function togglePassword(fieldId) {
	const field = document.getElementById(fieldId)
	field.type = field.type === 'password' ? 'text' : 'password'
}

const resetPasswordForm = document.getElementById('resetPasswordForm')
const newPassword = document.getElementById('new_password')
const confirmPassword = document.getElementById('confirm_password')
const passwordFeedback = document.getElementById('passwordFeedback')

function updatePasswordFeedback() {
	if (
		newPassword.value === confirmPassword.value &&
		newPassword.value !== ''
	) {
		passwordFeedback.textContent = 'Heslá sa zhodujú!'
		passwordFeedback.className = 'text-success mb-3'
		passwordFeedback.style.display = 'block'
	} else {
		passwordFeedback.textContent = 'Heslá sa nezhodujú!'
		passwordFeedback.className = 'text-danger mb-3'
		passwordFeedback.style.display = 'block'
	}
}

confirmPassword.addEventListener('input', updatePasswordFeedback)
newPassword.addEventListener('input', updatePasswordFeedback)

resetPasswordForm.addEventListener('submit', () => {
	if (newPassword.value !== confirmPassword.value) {
		passwordFeedback.textContent = 'Heslá sa nezhodujú!'
		passwordFeedback.className = 'text-danger mb-3'
		passwordFeedback.style.display = 'block'
	}
})
