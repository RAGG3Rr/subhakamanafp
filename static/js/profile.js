jQuery(function ($) {
  $( document ).ready(function() {
    const usertype= $('#id_user_type').find(":selected").val()
    count = $('#id_user').find(":selected").val()
    if (count){
      $('#id_user_type option:not(:selected)').attr('disabled', 'disabled')
      $('#id_user option:not(:selected)').attr('disabled', 'disabled')

      if (usertype === 'Retailer'){
        $('.field-approveWholesaler').css('display','none')
      }
      if (usertype === 'Wholesaler'){
        $('.field-approveRetailer').css('display','none')
      }
    }
  })
})