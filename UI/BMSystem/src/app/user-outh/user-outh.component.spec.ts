import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserOuthComponent } from './user-outh.component';

describe('UserOuthComponent', () => {
  let component: UserOuthComponent;
  let fixture: ComponentFixture<UserOuthComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UserOuthComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UserOuthComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
