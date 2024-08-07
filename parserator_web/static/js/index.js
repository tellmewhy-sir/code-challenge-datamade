/* TODO: Flesh this out to connect the form to the API and render results
   in the #address-results div. */
$(document).ready(function() {
   const $form = $('#js-parse-form')
   const $addressResults = $('#js-address-results')
   const $errorsEl = $('#js-errors')

   $form.on('submit', (e) => {
      e.preventDefault()
      $errorsEl.html('').hide()

      const address = $('#js-address').val()

      fetch(`/api/parse?address=${encodeURIComponent(address)}`)
      .then(res => res.json())
      .then((response) => {
         const { data, error } = response

         if (error) {
            $errorsEl.text(error.message)
            throw new Error()
         }
         const { address_components, address_type } = data
         const resultsTableHtml = Object.keys(address_components).map((tag) => (
            `
            <tr>
               <td>${tag}</td>
               <td>${address_components[tag]}</td>
            </tr>
            `
         )).join('')
         $('#js-results-table').html(resultsTableHtml)
         $('#js-parse-type').text(address_type)
         $addressResults.show()
      })
      .catch((err) => {
         $errorsEl.show()
      })
   })
})
