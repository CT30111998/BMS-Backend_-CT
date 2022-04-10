import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { NavBarComponent } from './nav-bar/nav-bar.component';
import { HomeComponent } from './home/home.component';
import { SignInComponent } from './user-outh/sign-in/sign-in.component';
import { SignUpComponent } from './user-outh/sign-up/sign-up.component';
import { BlogViewComponent } from './blog-view/blog-view.component';
import { WorkViewComponent } from './work-view/work-view.component';
import { SupportComponent } from './support/support.component';

const routes: Routes = [
  {path:'home',component:HomeComponent},
  {path:'Login',component:SignInComponent},
  {path:'Signup',component:SignUpComponent},
  {path:'blog',component:BlogViewComponent},
  {path:'me',component:WorkViewComponent},
  {path:'suppoer',component:SupportComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
