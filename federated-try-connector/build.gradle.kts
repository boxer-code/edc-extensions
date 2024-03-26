/*
 *  Copyright (c) 2020, 2021 Microsoft Corporation
 *
 *  This program and the accompanying materials are made available under the
 *  terms of the Apache License, Version 2.0 which is available at
 *  https://www.apache.org/licenses/LICENSE-2.0
 *
 *  SPDX-License-Identifier: Apache-2.0
 *
 *  Contributors:
 *       Microsoft Corporation - initial API and implementation
 *       Fraunhofer Institute for Software and Systems Engineering - added dependencies
 *       ZF Friedrichshafen AG - add dependency
 *
 */
@Suppress("DSL_SCOPE_VIOLATION")
plugins {
    `java-library`
    id("application")
    alias(libs.plugins.shadow)
}

dependencies {
    implementation(libs.edc.control.plane.api.client)
    implementation(libs.edc.control.plane.core)
    implementation(libs.edc.control.plane.api)
    implementation(libs.edc.data.plane.selector.core)
    implementation(libs.edc.api.observability)
    implementation(libs.edc.configuration.filesystem)
    implementation(libs.edc.iam.mock)
    implementation(libs.edc.dsp)
    implementation(libs.edc.data.plane.selector.api)
    implementation(libs.edc.data.plane.selector.client)
    implementation(libs.edc.transfer.data.plane)
    implementation(libs.edc.data.plane.spi)
    implementation(libs.edc.data.plane.core)
    implementation(libs.edc.data.plane.http)
    implementation(libs.edc.data.plane.kafka)
    implementation("black.ninia:jep:3.9.1")
    implementation(libs.edc.configuration.filesystem)
    implementation("com.google.code.gson:gson:2.10.1")
    implementation(libs.edc.management.api)
    implementation(project(":listener"))

    implementation(libs.jakarta.rsApi)
}

application {
    mainClass.set("org.eclipse.edc.boot.system.runtime.BaseRuntime")
}

tasks.withType<com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar> {
    mergeServiceFiles()
    archiveFileName.set("filesystem-config-connector.jar")
}
