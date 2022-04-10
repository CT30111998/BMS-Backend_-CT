import { variable } from '@angular/compiler/src/output/output_ast';
import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import { CustomValidators } from '../validation';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css'],
})
export class SignUpComponent implements OnInit {
  submit = false;
  success = '';
  constructor() {}

  empName = new FormControl('', [Validators.required, Validators.minLength(2)]);
  EmaiId = new FormControl('', [Validators.required, Validators.email]);
  password = new FormControl('', [
    Validators.required,
    Validators.pattern(
      '(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[$@$!%*?&])[A-Za-zd$@$!%*?&].{8,}'
    ),
    Validators.minLength(8),
  ]);
  conPass = new FormControl('', [Validators.required]);
  PhoneNo = new FormControl('', [
    Validators.required,
    Validators.pattern('[- +()0-9]{10,}'),
    Validators.minLength(10),
    Validators.maxLength(10),
  ]);

  formGrp = new FormGroup({
    empName:this.empName,
    EmaiId:this.EmaiId,
    password:this.password,
    conPass:this.conPass,
    PhoneNo:this.PhoneNo,
  });
  ngOnInit(): void {}

  get f() { return this.formGrp.controls; }

  onSubmit() {
    this.submit = true;
    if (this.formGrp.invalid) {
      return;
    }
    var val = {
      ...this.formGrp.value,
    };
    this.success = JSON.stringify(this.formGrp.value);
  }
}
