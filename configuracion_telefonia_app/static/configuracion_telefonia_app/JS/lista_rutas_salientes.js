/* Copyright (C) 2018 Freetech Solutions

 This file is part of OMniLeads

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see http://www.gnu.org/licenses/.

/*
 * Código js relacionado con vista de creación/modificación de IVRs
 */

function guardarOrden() {
    var orden = $("#rutas_salientes").sortable("toArray");
    $("#orden").val(JSON.stringify(orden));
    $("#form_ordenar").submit();
};

$( function() {
    $("#rutas_salientes").sortable();
});