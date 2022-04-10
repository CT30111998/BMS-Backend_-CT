import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavBarComponent } from './nav-bar/nav-bar.component';
import { HomeComponent } from './home/home.component';
import { UserOuthComponent } from './user-outh/user-outh.component';
import { SignInComponent } from './user-outh/sign-in/sign-in.component';
import { SignUpComponent } from './user-outh/sign-up/sign-up.component';
import { FooterComponent } from './footer/footer.component';
import { BlogViewComponent } from './blog-view/blog-view.component';
import { LikeViewComponent } from './blog-view/like-view/like-view.component';
import { CommentViewComponent } from './blog-view/comment-view/comment-view.component';
import { WorkViewComponent } from './work-view/work-view.component';
import { SupportComponent } from './support/support.component';
import { SideBarComponent } from './nav-bar/side-bar/side-bar.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    AppComponent,
    NavBarComponent,
    HomeComponent,
    UserOuthComponent,
    SignInComponent,
    SignUpComponent,
    FooterComponent,
    BlogViewComponent,
    LikeViewComponent,
    CommentViewComponent,
    WorkViewComponent,
    SupportComponent,
    SideBarComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule, 
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
