# README

- [README](#readme)
  - [Introduction](#introduction)

## Introduction

This is a repository of scripts that I use for our arma 3 server to make life easier.

For example downloading a steam collection using steamcmd, fixing mods capitalization issues...

## The Fucking Database

Because mongodevs are smoking some hard shit, they didnt provide a build for ubuntu 22.04 yet. so the solution for that is to use docker.
sadly docker circumvents UFW for linux by writing to iptables directly. to prevent outside access to your docker containers, run this command

iptables -I DOCKER-USER -i ext_if ! -s <your external interface ip> -j DROP

