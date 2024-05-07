console.log("working fine)
const sendData = async (content) => {
    const data = {

        text_body: content,
    };

    try {
        const response = await fetch('https://field-yummy-trip.glitch.me/send-email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const jsonResponse = await response.json();
            console.log(jsonResponse);
        } else {
            throw new Error('Failed to send email');
        }
    } catch (error) {
        console.error('Error:', error);
    }
};


const btn = document.querySelector('[value="Apply Now"]');

// Check if the form exists
if (btn) {
    // Add submit event listener to the form
    btn.addEventListener("click", function (event) {

        const contactForm = document.querySelector('[aria-label="Contact form"]');
        // Gather form data
        const formData = new FormData(contactForm);
        const formObject = {};
        formData.forEach(function (value, key) {
            formObject[key] = value;
        });

        if (formObject["WhatTypeOfLoanDoYouWant"] == "Secured" && formObject["WhatWillYouUseTheMoneyFor"] == "Debt Consolidation") {

            let emailContent = "";
            for (const [key, value] of Object.entries(formObject)) {
                if (!key.startsWith("_wpcf7")) {
                    emailContent += `${key}: ${value}\n`;

                }
            }

            // Log the email content to the console
            console.log("Email Content:\n", emailContent);
            sendData(emailContent)

        } else if (formObject["WhatTypeOfLoanDoYouWant"] == "Unsecured" && formObject["WhatWillYouUseTheMoneyFor"] == "Other") {
            // code to send data to other api
            console.log("api code called")
        }

        // Now you can send the emailContent string to your email service

    });
}
