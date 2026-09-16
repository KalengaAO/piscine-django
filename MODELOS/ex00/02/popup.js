function displayFormContents() {
	let out = ' '

	out += 'Firstname = ' + document.getElementById('firstname').value + '\n';
	out += 'Name = ' + document.getElementById('name').value + '\n';
	out += 'Phone = ' + document.getElementById('phone').value + '\n';
	out += 'Age = ' + document.getElementById('age').value + '\n';
	out += 'Email = ' + document.getElementById('email').value + '\n';

	out += 'Gender ';
	if (document.getElementById('gender_male').checked == true)
		out += ' male'// document.getElementById('gender_male').value;
	if (document.getElementById('gender_famale').checked == true)
		out += ' famale'// document.getElementById('gender_famale').value;
	if (document.getElementById('gender_other').checked == true)
		out += ' other' //document.getElementById('gender_other').values;
	out += '\n'

	if (document.getElementById('student').checked == true)
		out += 'Student at 42 = yes'
	else
		out += 'Student at 42 = no';
	alert(out);
}